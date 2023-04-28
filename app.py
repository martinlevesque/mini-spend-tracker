import calendar
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import text
from db import session
from lib import statement_decoder
from lib import date_util

# Data model

## rules
### - pattern (string)
### - category (string)

## spendings
### - date (datetime)
### - amount (float)
### - category (string)

### indexes: (spendings.date), (spendings.date, spendings.category)

app = Flask(__name__)

app.logger.debug('Booting server...')


# https://www.highcharts.com/blog/download/

@app.route('/')
def index():
    begin_date = request.args.get('begin_date')

    if not begin_date:
        begin_date = beginning_of_month_s()

    end_date = request.args.get('end_date')

    if not end_date:
        end_date = end_of_month_s()

    # with sqlalchemy, get the list of spendings grouped by category:
    raw_monthly_spendings = session.execute(text("""
        SELECT 
            strftime('%d-%m', date) AS 'date', 
            category, 
            SUM(amount) AS total_amount 
        FROM spendings 
        WHERE strftime('%Y-%m-%d', date) BETWEEN :begin_date AND :end_date
        GROUP BY strftime('%Y-%m', date), category; 
    """), {'begin_date': begin_date, 'end_date': end_date}).all()
    monthly_spendings = [{'date': r[0], 'category': r[1], 'total_amount': r[2]} for r in raw_monthly_spendings]

    return render_template('index.html',
                           monthly_spendings=monthly_spendings,
                           begin_date=begin_date,
                           end_date=end_date)


@app.route('/spendings/latest')
def latest_spendings():
    raw_spendings = session.execute(text("""
        SELECT date, amount, description, category
        FROM spendings 
        ORDER BY date DESC
        LIMIT 200
    """)).all()
    spendings = [{'date': r[0], 'amount': r[1], 'description': r[2], 'category': r[3]} for r in raw_spendings]

    return render_template('/spendings/latest.html', spendings=spendings)


@app.route('/spendings/delete')
def delete_spending():
    date = request.args.get('date')
    amount = request.args.get('amount')
    category = request.args.get('category')

    session.execute(text("""
        DELETE 
        FROM spendings 
        WHERE date = :date AND amount = :amount AND category = :category
    """),
                    {
                        'date': date,
                        'amount': amount,
                        'category': category
                    })

    session.commit()

    return redirect(url_for('latest_spendings'))


@app.route('/spendings/rules')
def list_rules():
    rules = session.execute(text('SELECT pattern, category FROM rules')).all()
    rules = [{'pattern': r[0], 'category': r[1]} for r in rules]

    return render_template('spendings/rules.html', rules=rules)


@app.route('/spendings/new')
def spendings_new():
    return render_template('spendings/new.html')


@app.route('/spendings/', methods=['POST'])
def post_spendings():
    result = []

    begin_date = request.form['begin_date']
    end_date = request.form['end_date']
    spendings = request.form['spendings']

    raw_available_rules = session.execute(text('SELECT pattern, category FROM rules')).all()
    available_rules = [{'pattern': r[0], 'category': r[1]} for r in raw_available_rules]
    current_id = 0

    for spending_line in spendings.split('\n'):
        current_id += 1
        cur_line = spending_line.strip()

        result_decode = statement_decoder.decode_line(cur_line, available_rules)

        if result_decode:
            result.append({
                'id': current_id,
                'status': 'success',
                'result': result_decode,
                'date': build_up_date_s(p_day=result_decode['day'], p_month=result_decode['month']),
                'line': cur_line
            })
        else:
            result.append({
                'id': current_id,
                'status': 'error',
                'result': {
                    'category': '',
                    'amount': '',
                    'rule': ''
                },
                'date': build_up_date_s(),
                'line': cur_line
            })

    return render_template('spendings/submission.html',
                           result=result,
                           nb_submissions=len(result),
                           categories=used_categories(),
                           )


@app.route('/spendings/submit', methods=['POST'])
def finalize_post_spendings():
    nb_submissions = int(request.form['nb_submissions'])

    for i in range(1, nb_submissions + 1):
        date = request.form[f'submission[{i}][date]']
        category = request.form[f'submission[{i}][category]']
        new_category = request.form[f'submission[{i}][new_category]']

        if new_category:
            category = new_category

        amount = request.form[f'submission[{i}][amount]']
        rule_pattern = request.form[f'submission[{i}][rule_pattern]']
        description = request.form[f'submission[{i}][description]']

        upsert_rule_pattern(rule_pattern, category)

        # insert in spendings
        if category != 'skip' and amount:
            result_count = session.execute(
                text('SELECT COUNT(*) as cnt FROM spendings WHERE date = :date AND category = '
                     ':category AND amount = :amount AND description = :description'),
                {
                    'date': date,
                    'category': category,
                    'amount': float(amount),
                    'description': description
                }
            ).one()

            if result_count.cnt == 0:
                session.execute(
                    text('INSERT INTO spendings (date, category, amount, description) VALUES (:date, :category, '
                         ':amount, :description)'),
                    {
                        'date': date,
                        'category': category,
                        'amount': float(amount),
                        'description': description
                    }
                )
                session.commit()
            else:
                app.logger.debug(f"Skipping insertion of {date} {category} {amount} {description}")

    return redirect(url_for('index'))


def build_up_date_s(p_day=None, p_month=None):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    if p_day:
        day = int(p_day)

    if p_month and date_util.convert_month(p_month):
        month = date_util.convert_month(p_month)

    return datetime(year, month, day).strftime('%Y-%m-%d')


def beginning_of_month_s():
    # in format YYYY-MM-DD
    return datetime.now().strftime('%Y-%m-01')


def end_of_month_s():
    res = calendar.monthrange(datetime.now().year, datetime.now().month)
    day = res[1]

    return datetime(datetime.now().year, datetime.now().month, day).strftime('%Y-%m-%d')


def used_categories():
    raw_categories = session.execute(text(
        'SELECT DISTINCT category FROM spendings UNION SELECT DISTINCT category FROM rules'
    )).all()

    db_categories = [r[0] for r in raw_categories]

    return list(set(db_categories + ['skip']))


def upsert_rule_pattern(rule_pattern, category):
    if not rule_pattern or not category:
        return

    result_count = session.execute(
        text('SELECT COUNT(*) as cnt FROM rules WHERE pattern = :pattern'),
        {
            'pattern': rule_pattern
        }
    ).one()

    if result_count.cnt == 0:
        session.execute(
            text('INSERT INTO rules (pattern, category) VALUES (:pattern, :category)'),
            {
                'pattern': rule_pattern,
                'category': category
            }
        )
        session.commit()
    else:
        app.logger.debug(f"Skipping insertion of {rule_pattern} {category}")
