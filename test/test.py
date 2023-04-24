import pytest
from deposite.validation_and_calculation import *


@pytest.mark.parametrize("test_input_date_validate, output_date_validate", [
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

def test_date_validate(test_input_date_validate, output_date_validate):
    assert date_validate(test_input_date_validate) == output_date_validate




def test_periods_validate():
    # Проверка на корректный тип переменной periods
    result, error = periods_validate("test")
    assert not result
    assert error == {"error": "data type 'periods' mismatch: not integer"}

    # Проверка на значение переменной periods, входящее в диапазон
    result, error = periods_validate(0)
    assert not result
    assert error == {"error": "the value of the field 'periods' is out of the allowed range: [1, 60]"}

    # Проверка на значение переменной periods, выходящее за пределы диапазона
    result, error = periods_validate(100)
    assert not result
    assert error == {"error": "the value of the field 'periods' is out of the allowed range: [1, 60]"}

    # Проверка на корректный тип результата и ошибки
    result, error = periods_validate(30)
    assert result
    assert error == {}











