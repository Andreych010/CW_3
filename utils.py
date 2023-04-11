from datetime import datetime
import json
import operator

file_name = 'operations.json' #переменная с файлом, данными json, аргумент для data_json
executed = 'EXECUTED' #переменная с полем 'EXECUTED' для функции parse


def data_json(file_name):
    '''
:param file_name: файл с данными
:return: возвращает данные json
    '''
    with open(file_name, encoding='utf-8') as f:
        response = f.read()
    return json.loads(response)

def sort_data(respons):
    '''
сортирует операции по дате
:param respons: данные по операциям
:return: возвращает 5 отсортированых по дате операции
    '''
    sort_ = [date for date in respons if 'date' in date]
    sort_.sort(key=operator.itemgetter('date'), reverse=True)
    return sort_


def get_payment_type(payment: str):
    '''
возвращает замаскированный номер карты и счёта
    '''
    if 'счет' in payment.lower():
        return f'{payment[:5]}**{payment[-4:]}'
    else:
        payment_type = f'{payment.split()[len(payment.split()) - 1]}'
        card_type = f'{payment.replace(f" {payment_type}", "")}'
        payment_type = payment_type[:-10] + '** **** ' + payment_type[12:]
        payment_type = f'{card_type} {payment_type[:4]} {payment_type[4:]}'
        return payment_type


def parse(res):
    '''
возвращает 5 последних операций, отсортированных executed
:param res: отсортированные по дате операции
    '''

    result = ''
    count = 0
    for i in res:
        if len(i) > 0 and i['state'] == executed:
            round_result = ''
            datetime_str = i['date'].split('T')[0]
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d').date().strftime('%d.%m.%Y')
            cost = f'{i["operationAmount"]["amount"]} {i["operationAmount"]["currency"]["name"]}'
            round_result += f'{datetime_object} {i["description"]}\n'
            if 'открытие' in i['description'].lower():
                round_result += f'{get_payment_type(i["to"])}'
            else:
                round_result += f'{get_payment_type(i["from"])} -> {get_payment_type(i["to"])}'
            round_result += f'\n{cost}\n\n'

            result += round_result
            count += 1
        if count == 5: break
    return result
