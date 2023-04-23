from flask import Flask, render_template, request
from sqlalchemy import text
from db import session
from lib import statement_decoder

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
    return render_template('index.html')


@app.route('/spendings/new')
def spendings_new():
    return render_template('spendings/new.html')

@app.route('/spendings/', methods=['POST'])
def post_spendings():
    result = []

    # print body
    # print request.form
    print(f"date: {request.form}")
    begin_date = request.form['begin_date']
    end_date = request.form['end_date']
    spendings = request.form['spendings']

    raw_available_rules = session.execute(text('SELECT pattern, category FROM rules')).all()
    available_rules = [ { 'pattern': r[0], 'category': r[1] } for r in raw_available_rules]

    for spending_line in spendings.split('\n'):
        cur_line = spending_line.strip()

        result_decode = statement_decoder.decode_line(cur_line, available_rules)

        if result_decode:
            result.append({
                'status': 'success',
                'result': result_decode,
                'line': cur_line
            })
        else:
            result.append({
                'status': 'error',
                'line': cur_line
            })

    return render_template('spendings/submission.html', result=result)
