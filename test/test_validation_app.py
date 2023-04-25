import pytest
from deposite import *
import datetime


@pytest.mark.parametrize("input, output", [
    ('10.01.2021', (True, {})),
    (1, (False, {'error': 'data type "date" mismatch: not string'})),
    ('23.04.2023', (True, {})),
    ('31.02.2023', (False, {'error': "incorrect data format 31.02.2023, correct type is '%d.%m.%Y'"})), 
    (True, (False, {'error': 'data type "date" mismatch: not string'})),
    (5.123, (False, {'error': 'data type "date" mismatch: not string'})),
    ({'10.01.2021'}, (False, {'error': 'data type "date" mismatch: not string'})),
    (('14.0.2019'), (False, {'error': "incorrect data format 14.0.2019, correct type is '%d.%m.%Y'"})),
    ([11], (False, {'error': 'data type "date" mismatch: not string'}))
])


def test_date_validate(input, output):
    assert date_validate(input) == output



@pytest.mark.parametrize("input, output", [
    (1, (True, {})),
    (60, (True, {})),
    (33, (True, {})),
    (-1, (False, {'error': "the value of the field 'periods' is out of the allowed range: [1, 60]"})),
    (80, (False, {'error': "the value of the field 'periods' is out of the allowed range: [1, 60]"})),
    (1.5, (False, {'error': 'data type "periods" mismatch: not integer'})),
    ('10', (False, {'error': 'data type "periods" mismatch: not integer'}))
])


def test_periods_validate(input, output):
    assert periods_validate(input) == output



@pytest.mark.parametrize("input, output", [
    (10000, (True, {})),
    (3000000, (True, {})),
    (50000, (True, {})),
    (999, (False, {'error': "the value of the field 'amount' is out of the allowed range: [10000, 3000000]"})),
    (5000000, (False, {'error': "the value of the field 'amount' is out of the allowed range: [10000, 3000000]"})),
    ('10000', (False, {'error': 'data type "amount" mismatch: not integer or float'})),
])


def test_amount_validation(input, output):
    assert amount_validation(input) == output



@pytest.mark.parametrize("input, output", [
    (1, (True, {})),
    (8, (True, {})),
    (4.9, (True, {})),
    (9, (False, {'error': "the value of the field 'rate' is out of the allowed range: [1, 8]"})),
    (0.5, (False, {'error': "the value of the field 'rate' is out of the allowed range: [1, 8]"})),
    ('3', (False, {'error': 'data type "rate" mismatch: not integer or float'}))
])


def test_rate_validation(input, output):
    assert rate_validation(input) == output




@pytest.mark.parametrize("input, output", [
    (10050.00, 10050),
    (10050.0, 10050),
    (10049.9999999999, 10050),
    (10049.36532234, 10049.37)
])



def test_round_number(input, output):
    assert round_number(input) == output




@pytest.mark.parametrize("input, output", [
    ('12.01.2022', datetime.date(2022, 1, 31)),
    ('01.02.2022', datetime.date(2022, 2, 28)),
    ('31.12.2023', datetime.date(2023, 12, 31))
])



def test_get_last_day_of_current_month(input, output):
    assert get_last_day_of_current_month(input) == output




@pytest.mark.parametrize("input, output", [

    ({"date": "31.01.2021",
    "periods": 1,
    "amount": 10000,
    "rate": 1}, {'31.01.2021': 10008.33}),

    ({"date": "01.01.2021",
    "periods": 2,
    "amount": 10000,
    "rate": 6}, {'31.01.2021': 10050, '28.02.2021': 10100.25}),

    ({"date": "01.01.2021",
    "periods": 3,
    "amount": 3000000,
    "rate": 8}, {'31.01.2021': 3020000, '28.02.2021': 3040133.33, '31.03.2021': 3060400.89})
])




def test_get_deposite_result(input, output):
    assert get_deposite_result(input) == output




@pytest.mark.parametrize("input, output", [

    ({"date": "01.01.2021",
    "periods": 3,
    "amount": 3000000,
    "rate": 8}, (True, {'31.01.2021': 3020000, 
                        '28.02.2021': 3040133.33, 
                        '31.03.2021': 3060400.89})),

    ({"date": "24.12.2023",
    "periods": 6,
    "amount": 10101,
    "rate": 4.9}, (True, {'31.12.2023': 10142.25,
                        '31.01.2024': 10183.66,
                        '29.02.2024': 10225.24,
                        '31.03.2024': 10267,
                        '30.04.2024': 10308.92,
                        '31.05.2024': 10351.01})),

    ({"date": "24.12.2020",
    "periods": 12,
    "amount": 10000,
    "rate": 0}, (False, {'error': 
                         ["the value of the field 'rate' is out of the allowed range: [1, 8]"]})),

    ({"date": "24.12.2020",
    "periods": 61,
    "amount": 5000,
    "rate": '0'}, (False,{'error': 
                          ["the value of the field 'periods' is out of the allowed range: [1, 60]",
                            "the value of the field 'amount' is out of the allowed range: [10000, 3000000]",
                            'data type "rate" mismatch: not integer or float']}))
])




def test_aggregate_validation_and_calculating(input, output):
    assert aggregate_validation_and_calculating(input)[0] == output[0]
