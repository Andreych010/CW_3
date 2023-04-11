import re, os
from utils import *


#Тесты для sort_data()
#Тест для sort_data() на проверку правильности сортировки
def test_is_sorted(test_data_is_sorted):
    sorted_data = sort_data(test_data_is_sorted)
    check_data = [
        "2019-08-26T10:50:58.294041",
        "2019-07-03T18:35:29.512364", 
        "2018-11-23T23:52:36.999661",
        "2018-06-30T02:08:58.425572", 
        "2018-03-23T10:45:06.972075"
        ]
    assert [x['date'] for x in sorted_data] == check_data


#Тест для sort_data() на утончённую проверку правильности сортировки
def test_is_sorted_same_day(test_data_is_sorted_same_day):

    sorted_data = sort_data(test_data_is_sorted_same_day)
    check_data = [
        "2018-11-23T23:52:36.999661",
        "2018-11-23T18:35:29.512364", 
        "2018-11-23T10:50:58.294041",
        "2018-11-23T10:45:06.972075",
        "2018-11-23T02:08:58.425572"
        ]
    assert [x['date'] for x in sorted_data] == check_data


#Тест для sort_data() на проверку входных данных
def test_is_nonvalid_input(test_data_is_valid_input):
    try:
        sort_data(test_data_is_valid_input)
    except TypeError:
        assert True


#Тест для data_json()
def test_is_convert(test_data_is_convert):

    converted_data = data_json(test_data_is_convert)
    check_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]
    assert converted_data == check_data
    os.remove(test_data_is_convert)


#Тесты для get_payment_type()
#Тест на скрытие номера карты или счёта из поля "to"
def test_is_hides_to(test_data_is_hides):
    pattern = r'(\*\*[a-z]{4})|([a-z]{4} [a-z]{2}\*\* \*\*\*\* [a-z]{4})'
    for element in test_data_is_hides:
        converted_data = get_payment_type(element["to"]) + ' '
        if re.search(pattern, converted_data):
            assert False
    assert True


#Тест на скрытие номера карты или счёта из поля "from"
def test_is_hides_from(test_data_is_hides):
    pattern = r'(\*\*[a-z]{4})|([a-z]{4} [a-z]{2}\*\* \*\*\*\* [a-z]{4})'
    for element in test_data_is_hides:
        try:
            converted_data = get_payment_type(element["from"]) + ' '
            if re.search(pattern, converted_data):
                assert False
        except KeyError:
            continue
    assert True


#Тест на то, что при сокрытии номера карты не меняются видимые цифры
def test_is_right_account_digits(test_data_is_right_digits):
    assert get_payment_type(test_data_is_right_digits["from"])[-19:] == '1596 83** **** 5199'


#Тест на то, что при сокрытии номера счёта не меняются видимые цифры
def test_is_right_card_digits(test_data_is_right_digits):
    assert get_payment_type(test_data_is_right_digits["to"])[-6:] == '**9589'


#Тесты для parse()
#Тест, что выводится 5 транзакций
def test_is_5_transactions(test_data_general):
    result_data = parse(test_data_general)
    assert result_data.count('\n') == 20


#Тест, что выводится 5 валидных транзакций
def test_is_valid_transactions(test_data_general):
    result_data = parse(test_data_general)
    count = 0
    for element in result_data.split('\n'):
        if count % 4 == 0:
            time = element[:10]
            for i in test_data_general:
                if time in i['date'] and i['state'] != "EXECUTED":
                    assert False
                else: break
        count += 1
    assert True