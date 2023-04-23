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

