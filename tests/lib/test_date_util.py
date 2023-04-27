from lib import date_util


def test_date_util_convert_month_happy_path():
    assert date_util.convert_month('12') == 12


def test_date_util_convert_month_invalid_int():
    assert date_util.convert_month('fff') is None


def test_date_util_convert_month_english_abbr():
    assert date_util.convert_month('feb') == 2


def test_date_util_convert_month_english_long_name():
    assert date_util.convert_month('february') == 2


def test_date_util_convert_month_french_abbr():
    assert date_util.convert_month('janv') == 1
    assert date_util.convert_month('févr') == 2
    assert date_util.convert_month('mars') == 3
    assert date_util.convert_month('avr') == 4
    assert date_util.convert_month('mai') == 5
    assert date_util.convert_month('juin') == 6
    assert date_util.convert_month('juil') == 7
    assert date_util.convert_month('août') == 8
    assert date_util.convert_month('sept') == 9
    assert date_util.convert_month('oct') == 10
    assert date_util.convert_month('nov') == 11
    assert date_util.convert_month('déc') == 12


def test_date_util_convert_month_french_long():
    assert date_util.convert_month('janvier') == 1
    assert date_util.convert_month('février') == 2
    assert date_util.convert_month('mars') == 3
    assert date_util.convert_month('avril') == 4
    assert date_util.convert_month('mai') == 5
    assert date_util.convert_month('juin') == 6
    assert date_util.convert_month('juillet') == 7
    assert date_util.convert_month('août') == 8
    assert date_util.convert_month('septembre') == 9
    assert date_util.convert_month('octobre') == 10
    assert date_util.convert_month('novembre') == 11
    assert date_util.convert_month('décembre') == 12
