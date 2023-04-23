from lib import statement_decoder
import json


def test_statement_decoder_decode_line_happy_path():
    pattern = json.dumps({
        'pattern': '^begin (\\d+) test$',
        'variable_positions': {
            'day': 0
        }
    })

    rules = [
        {
            'pattern': pattern,
            'category': 'default'
        }
    ]

    expected_result = {
        'category': 'default',
        'day': '12'
    }
    assert statement_decoder.decode_line('begin 12 test', rules) == expected_result


def test_statement_decoder_decode_line_given_no_match():
    pattern = json.dumps({
        'pattern': '^begin (\\d+) test$',
        'variable_positions': {
            'day': 0
        }
    })

    rules = [
        {
            'pattern': pattern,
            'category': 'default'
        }
    ]

    assert not statement_decoder.decode_line('invalid 23', rules)


def test_statement_decoder_decode_line_multiple_variables():
    pattern = json.dumps({
        'pattern': '^begin (\\d+) (.{3}) test$',
        'variable_positions': {
            'day': 0,
            'month': 1
        }
    })

    rules = [
        {
            'pattern': pattern,
            'category': 'default'
        }
    ]

    expected_result = {
        'category': 'default',
        'day': '12',
        'month': 'mar'
    }
    assert statement_decoder.decode_line('begin 12 mar test', rules) == expected_result


def test_statement_decoder_decode_line_multiple_patterns():
    pattern = json.dumps({
        'pattern': '^begin (\\d+) (.{3}) test$',
        'variable_positions': {
            'day': 0,
            'month': 1
        }
    })

    rules = [
        {
            'pattern': json.dumps({
                'pattern': 'test',
                'variable_positions': {}
            }),
            'category': 'test'
        },
        {
            'pattern': pattern,
            'category': 'default'
        }
    ]

    expected_result = {
        'category': 'default',
        'day': '12',
        'month': 'mar'
    }
    assert statement_decoder.decode_line('begin 12 mar test', rules) == expected_result


def test_statement_decoder_decode_line_skipping_pattern():
    pattern = json.dumps({'pattern': '^begin (\\d+) (.{3}) test$'})

    rules = [
        {
            'pattern': pattern,
            'category': 'skip'
        }
    ]

    expected_result = {
        'category': 'skip'
    }
    assert statement_decoder.decode_line('begin 12 mar test', rules) == expected_result
