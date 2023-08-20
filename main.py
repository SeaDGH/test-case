import json
from os import path
import typing


def start():
    if not path.exists('./dictionary.json'):
        print('JSON файл не найдет!\nСоздаю новый файл...')
        json_data = [{
            1: {}
        }]
        with open('./dictionary.json', 'w', encoding='utf8') as file:
            file.write((json.dumps(json_data, indent=2, ensure_ascii=False)))
            file.close()
    while True:
        answer = input('Какое действие хотите выполнить?\n'
                       '1 - Просмотреть текущие записи в справочнике\n'
                       '2 - Добавить новую запись в справочник\n'
                       '3 - Редактировать текущую запись в справочнике\n'
                       '4 - Поиск записей по справочнику\n')
        if answer == '1':
            view()
        elif answer == '2':
            add()
        elif answer == '3':
            first_level_edit()
        elif answer == '4':
            search()
        else:
            print('Неизвестная команда!\n')


def view(edit_check: bool = False):
    print('\nОткрываю справочник для получения записей...')
    with open('./dictionary.json', encoding='utf8') as file:
        data = json.load(file)[0]
        keys = list(data.keys())
        if not data.get(keys[-1], {}):
            print('Справочник пуст!\n')
        else:
            for record in data:
                print('\nЗапись №{}\n'.format(record))
                for key in data[record]:
                    print('{}: {}'.format(key, data[record][key]))
                    file.close()
            if edit_check:
                print('\nПерехожу к изменениям записей...\n')
                second_level_edit()
        input('\nДля возврата в меню нажмите Enter\n')


def add():
    print('\nОткрываю справочник для внесения новой записи...\n')
    with open('./dictionary.json', encoding='utf8') as file:
        data = json.load(file)[0]
        file.close()
    print('Введите данные')
    while True:
        try:
            surname, name, middle_name = input('ФИО:\n').split()
            break
        except ValueError:
            pass
        print('ФИО указано в неправильном формате\n'
              'Пример:\n'
              'Иванов Иван Иванович\n')
    organization = input('Название организации:\n')
    work_phone = input('Рабочий телефон:\n')
    personal_phone = input('Сотовый телефон:\n')
    json_data = {
        'Фамилия': surname,
        'Имя': name,
        'Отчество': middle_name,
        'Организация': organization,
        'Рабочий телефон': work_phone,
        'Сотовый телефон': personal_phone,
    }
    with open('./dictionary.json', 'w', encoding='utf8') as file:
        keys = list(data.keys())
        if not data.get(keys[-1], {}):
            data[str(keys[-1])] = json_data
            json.dump(data, file, indent=2, ensure_ascii=False)
            print('Добавлена новая запись №{}!'.format(str(keys[-1])))
            print('Переход в меню...\n')
        else:
            new_record = int(keys[-1]) + 1
            data[str(new_record)] = json_data
            json.dump(data, file, indent=2, ensure_ascii=False)
            print('Добавлена новая запись №{}!'.format(new_record))
            print('Переход в меню...\n')


def first_level_edit():
    while True:
        review = input('\nПросмотреть текущие записи?(Да\Нет)\n')
        try:
            if review.lower() == 'да':
                view(edit_check=True)
                break
            elif review.lower() == 'нет':
                print('\nОткрываю справочник для изменения записи...\n')
                second_level_edit()

            else:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('Неизвестная команда!\n'
                  'Попробуйте снова\n')
            pass


def second_level_edit():
    with open('./dictionary.json', encoding='utf8') as file:
        data = json.load(file)[0]
    while True:
        try:
            record_num = input('Выберите запись для редактирования\n')
            print('Открываю запись №{}\n'.format(record_num))
            for key in data[record_num]:
                print('{}: {}'.format(key, data[record_num][key]))
            while True:
                try:
                    edit_line = input('\nВыберите строку для редактирования\n')
                    if edit_line.lower() == 'фамилия':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Фамилия'] = new_value
                    elif edit_line.lower() == 'имя':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Имя'] = new_value
                    elif edit_line.lower() == 'отчество':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Отчество'] = new_value
                    elif edit_line.lower() == 'организация':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Организация'] = new_value
                    elif edit_line.lower() == 'рабочий телефон':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Рабочий телефон'] = new_value
                    elif edit_line.lower() == 'сотовый телефон':
                        new_value = input('Введите новое значение: ')
                        data[record_num]['Сотовый телефон'] = new_value
                    else:
                        raise KeyboardInterrupt
                    print('\nЗапись с новыми значениями\n')
                    for key in data[record_num]:
                        print('{}: {}'.format(key, data[record_num][key]))
                    confirmation = input('\nСохранить изменения?\n')
                    if confirmation.lower() == 'да':
                        with open('./dictionary.json', 'a', encoding='utf8') as file:
                            json.dump(data, file, indent=2, ensure_ascii=False)
                            print('Изменения сохранены!')
                            print('Переход в меню...\n')
                    elif confirmation.lower() == 'нет':
                        file.close()
                        print('Отменяю последние изменения...')
                        print('Переход в меню...\n')
                except KeyboardInterrupt:
                    print('Неизвестное поле!\n'
                          'Попробуйте снова\n')

        except KeyError:
            print('Записи с номером {} не существует'.format(record_num))
            review = input('Хотите проверить какие записи существуют?(Да\Нет)\n')
            if review.lower() == 'да':
                view(edit_check=True)
            elif review.lower() == 'нет':
                pass


def search():
    pass


if __name__ == "__main__":
    start()
