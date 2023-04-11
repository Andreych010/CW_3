from utils import parse, sort_data, data_json

file_name = 'operations.json' #переменная с файлом, данными json, аргумент для data_json

def main():
    '''
основная функция, выводит на экран список из 5 последних выполненных клиентом операций
    '''
    data = data_json(file_name)
    data = sort_data(data)
    data = parse(data)
    print(data)

if __name__ == '__main__':
    main()