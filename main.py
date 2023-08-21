import json
from sys import exit
from os import path


def start() -> None:
    """
    Функция start открывает навигационное меню телефонного справочника.
    Является главной функцией, из которой открываются другие функции:
    view
    add
    edit(first_level_edit и second_level_edit)
    search(first_level_search и second_level_search)
    При неправильном запросе отправляет ответ и просит ввести запрос заново.
    :return None:
    """
    if not path.exists('./dictionary.json'):
        print('JSON файл не найдет!\nСоздаю новый файл...')
        json_data: dict = {
            1: {}
        }
        with open('./dictionary.json', 'w', encoding='utf8') as file:
            file.write((json.dumps(json_data, indent=2, ensure_ascii=False)))
            file.close()
    while True:
        answer: str = input('Какое действие хотите выполнить?\n'
                            '1 - Просмотреть текущие записи в справочнике\n'
                            '2 - Добавить новую запись в справочник\n'
                            '3 - Редактировать текущую запись в справочнике\n'
                            '4 - Поиск записей по справочнику\n'
                            'Для выхода из программы напишите "Выход"\n')
        if answer == '1':
            view()
        elif answer == '2':
            add()
        elif answer == '3':
            first_level_edit()
        elif answer == '4':
            first_level_search()
        elif answer.lower() == 'выход':
            exit()
        else:
            print('Неизвестная команда!\n')


def view(edit_check: bool = False) -> None:
    """
    Функция view служит для вывода всех существующих записей.
    Если записей нет, то выводит сообщение о том что справочник пуст.
    Так же функция является вспомогательной функцией для edit.
    При наличии edit_check запускает функцию second_level_edit
    :param edit_check:
    :return None:
    """
    print('\nОткрываю справочник для получения записей...')
    with open('./dictionary.json', encoding='utf8') as file:
        data: dict = json.load(file)
        keys: list = list(data.keys())
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


def add() -> None:
    """
    Функция add добавляет новую запись в справочник.
    В процессе выполнения запрашивает у пользователя данный для новой записи:
    Фамилию
    Имя
    Отчество
    Организацию
    Рабочий и сотовый телефоны
    :return None:
    """
    print('\nОткрываю справочник для внесения новой записи...\n')
    with open('./dictionary.json', encoding='utf8') as file:
        data = json.load(file)
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
    organization: str = input('Название организации:\n')
    work_phone: str = input('Рабочий телефон:\n')
    personal_phone: str = input('Сотовый телефон:\n')
    json_data = {
        'Фамилия': surname,
        'Имя': name,
        'Отчество': middle_name,
        'Организация': organization,
        'Рабочий телефон': work_phone,
        'Сотовый телефон': personal_phone,
    }
    with open('./dictionary.json', 'w', encoding='utf8') as file:
        keys: list = list(data.keys())
        if not data.get(keys[-1], {}):
            data[str(keys[-1])]: dict = json_data
            json.dump(data, file, indent=2, ensure_ascii=False)
            print('Добавлена новая запись №{}!'.format(str(keys[-1])))
            print('Переход в меню...\n')
        else:
            new_record: int = int(keys[-1]) + 1
            data[str(new_record)]: dict = json_data
            json.dump(data, file, indent=2, ensure_ascii=False)
            print('Добавлена новая запись №{}!'.format(new_record))
            print('Переход в меню...\n')


def first_level_edit() -> None:
    """
    Первая(вспомогательная) функция из семейства edit.
    Функция first_level_edit запрашивает у пользователя нужно ли ему показать текущие записи:
    Если нет то перенаправляет на second_level_edit.
    Если да то открывает функцию view.
    Есть обработка на неправильный запрос.
    :return None:
    """
    while True:
        review: str = input('\nПросмотреть текущие записи?(Да\Нет)\n')
        try:
            if review.lower() == 'да':
                view(edit_check=True)
                break
            elif review.lower() == 'нет':
                second_level_edit()
                break
            else:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('Неизвестная команда!\n'
                  'Попробуйте снова\n')
            pass


def second_level_edit() -> None:
    """
    Вторая(главная) функция из семейства edit.
    Запрашивает данные у пользователя для редактирования.
    В частности строку в которую нужно внести изменения и новое значение.
    Далее подтверждение изменения:
    Если пользователь согласен то перезаписывает данные в справочнике.
    Если нет, то данные не сохраняются.
    Есть обработка на неправильный запрос.
    :return None:
    """
    print('\nОткрываю справочник для изменения записи...\n')
    with open('./dictionary.json', encoding='utf8') as file:
        data: dict = json.load(file)
    while True:
        try:
            record_num: str = input('Выберите запись для редактирования\n')
            print('Открываю запись №{}\n'.format(record_num))
            for key in data[record_num]:
                print('{}: {}'.format(key, data[record_num][key]))
            while True:
                try:
                    edit_line: str = input('\nВыберите строку для редактирования\n')
                    if edit_line.lower() == 'фамилия':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Фамилия']: str = new_value
                    elif edit_line.lower() == 'имя':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Имя']: str = new_value
                    elif edit_line.lower() == 'отчество':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Отчество']: str = new_value
                    elif edit_line.lower() == 'организация':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Организация']: str = new_value
                    elif edit_line.lower() == 'рабочий телефон':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Рабочий телефон']: str = new_value
                    elif edit_line.lower() == 'сотовый телефон':
                        new_value: str = input('Введите новое значение: ')
                        data[record_num]['Сотовый телефон']: str = new_value
                    else:
                        raise KeyboardInterrupt
                    print('\nЗапись с новыми значениями\n')
                    for key in data[record_num]:
                        print('{}: {}'.format(key, data[record_num][key]))
                    confirmation: str = input('\nСохранить изменения?\n')
                    if confirmation.lower() == 'да':
                        with open('./dictionary.json', 'w', encoding='utf8') as file:
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
                finally:
                    break
        except KeyError:
            print('Записи с номером {} не существует'.format(record_num))
            review: str = input('Хотите проверить какие записи существуют?(Да\Нет)\n')
            if review.lower() == 'да':
                view(edit_check=True)
            elif review.lower() == 'нет':
                pass
        finally:
            break


def first_level_search() -> None:
    """
    Первая функция из семейства search.
    Выводит примеры строк по которым можно провести поиск.
    Далее запрашивает у пользователя по какой строке будет идти поиск.
    Передает информацию в second_level_search.
    Есть обработка на неправильный запрос.
    :return None:
    """
    while True:
        try:
            print('\nФамилия\n'
                  'Имя\n'
                  'Отчество\n'
                  'Организация\n'
                  'Рабочий телефон\n'
                  'Сотовый телефон')
            search_for: str = input('\nВыберите строку для поиска\n')

            if search_for.lower() in ['фамилия',
                                      'имя',
                                      'отчество',
                                      'организация',
                                      'рабочий телефон',
                                      'сотовый телефон']:
                second_level_search(search_for.lower())
            else:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('\nНеизвестное поле!\n'
                  'Попробуйте снова\n')


def second_level_search(line: str) -> None:
    """
    Вторая функция из семейства search.
    Выводит записи из словаря, которые подходят по критериям поиска.
    Запрашивает значение по которому нужно провести поиск.
    Если записи по заданным критериям не нашлось, то информирует об этом
    :param line:
    :return None:
    """
    print('\nОткрываю справочник для поиска записи(ей)...\n')
    with open('./dictionary.json', "r", encoding='utf8') as file:
        data: dict = json.load(file)
    search_for: str = input('Введите значение которое нужно найти\n')
    flag: bool = True
    for record in data:
        for key in data[record]:
            if line == key.lower():
                if search_for.lower() == data[record][key]:
                    flag: bool = False
                    print('Запись №{}\n'.format(record))
                    for key_ in data[record]:
                        print('{}: {}'.format(key_, data[record][key_]))
                    print()
    if flag:
        print('\nЗаписей по таким критериям не найдена')


if __name__ == "__main__":
    start()
