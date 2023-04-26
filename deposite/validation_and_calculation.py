from datetime import date, datetime, timedelta
import calendar
import requests


def date_validate(date_value, date_type='%d.%m.%Y') -> tuple:

    '''
    Возвращает результат валидации поля date в формате (flag, {error: describe})
    '''

    flag = False
    error_dict = {}

    if not isinstance(date_value, str):
        error_dict['error'] = f'data type "date" mismatch: not string'
        return flag, error_dict

    try:
        datetime.strptime(date_value, date_type)
    except:
        error_dict['error'] = f"incorrect data format {date_value}, correct type is '{date_type}'"
        
        return flag, error_dict

    flag = True

    return flag, error_dict



def periods_validate(periods, thresholds=(1, 60)) -> tuple:

    '''
    Возвращает результат валидации поля periods в формате (flag, {error: describe})
    '''

    flag = False
    error_dict = {}

    if not isinstance(periods, int):
        error_dict['error'] = f'data type "periods" mismatch: not integer'
        return flag, error_dict

    if not (thresholds[0] <= periods <= thresholds[1]):
        error_dict['error'] = f"the value of the field 'periods' is out of the allowed range: [{thresholds[0]}, {thresholds[1]}]"
        return flag, error_dict
    
    flag = True
    
    return flag, error_dict 



def amount_validation(amount, thresholds=(10000, 3000000)) -> tuple:
    
    '''
    Возвращает результат валидации поля amount в формате (flag, {error: describe})
    '''

    flag = False
    error_dict = {}

    if not isinstance(amount, (int, float)):
        error_dict['error'] = f'data type "amount" mismatch: not integer or float'
        return flag, error_dict
    
    if not (thresholds[0] <= amount <= thresholds[1]):
        error_dict['error'] = f"the value of the field 'amount' is out of the allowed range: [{thresholds[0]}, {thresholds[1]}]"
        return flag, error_dict
    
    flag = True
    
    return flag, error_dict



def rate_validation(rate, thresholds=(1, 8)) -> tuple:
    
    '''
    Возвращает результат валидации поля rate в формате (flag, {error: describe})
    '''

    flag = False
    error_dict = {}

    if not isinstance(rate, (int, float)):
        error_dict['error'] = f'data type "rate" mismatch: not integer or float'
        return flag, error_dict
    
    if not (thresholds[0] <= rate <= thresholds[1]):
        error_dict['error'] = f"the value of the field 'rate' is out of the allowed range: [{thresholds[0]}, {thresholds[1]}]"
        return flag, error_dict
    
    flag = True
    
    return flag, error_dict



def round_number(number):

    '''
    Возвращает округленное число до двух знаков; округляет до целого
    '''

    if round(number, 2) == round(number):
        return round(number)
    
    return round(number, 2)



def calculation_of_the_deposit(deposit, rate):
    
    '''
    Возвращает результат расчета депозита на 1 месяц
    '''

    return deposit * (1 + rate / 1200)



def get_last_day_of_current_month(date_) -> datetime:
    
    '''
    Возвращает дату последнего дня месяца в формате datetime
    '''

    if isinstance(date_, str):
        date_ = datetime.strptime(date_, '%d.%m.%Y')
    
    last_day = calendar.monthrange(date_.year, date_.month)[1]
    last_day_of_the_month = date(date_.year, date_.month, last_day)
    
    return last_day_of_the_month
    



def get_deposite_result(json_data: dict) -> dict:
    
    '''
    Возвращает результат расчета депозита за весь период
    '''

    deposite_result = {}

    periods, deposite_date = json_data['periods'], json_data['date']
    amount, rate = json_data['amount'], json_data['rate']

    for period in range(periods):
        deposite_result[get_last_day_of_current_month(deposite_date).strftime('%d.%m.%Y')] = round_number(calculation_of_the_deposit(amount, rate))
        amount = calculation_of_the_deposit(amount, rate)
        deposite_date = get_last_day_of_current_month(deposite_date) + timedelta(days=1)

    return deposite_result



def aggregate_validation_and_calculating(json_data: dict) -> tuple:
        
    '''
    Возвращает результат расчета депозита в случае прохождении валидации, иначе возвращает ошибку 
    '''

    if all([date_validate(json_data['date'])[0],\
           periods_validate(json_data['periods'])[0],\
           amount_validation(json_data['amount'])[0],\
           rate_validation(json_data['rate'])[0]]):

        return True, get_deposite_result(json_data)

    error_list = [error['error'] for error in 
                    [date_validate(json_data['date'])[1],\
                    periods_validate(json_data['periods'])[1],\
                    amount_validation(json_data['amount'])[1],\
                    rate_validation(json_data['rate'])[1]] if error]
                    
    return False, {'error': error_list}



def requests_response_to_app(input_data: dict, 
                             link='http://127.0.0.1:5000/deposite', 
                             headers={'Content-Type': 'application/json'}):
        
    '''
    Возвращает ответ приложения на запрос расчета депозита
    '''

    return requests.post(link, json=input_data, headers=headers).json()
