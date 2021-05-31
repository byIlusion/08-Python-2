import locale


def file_create(file_name, lines=[], encoding=None):
    with open(file_name, 'w', encoding=encoding) as fn:
        fn.write('\n'.join(lines))
        print(f'Файл {file_name} записан')


def file_read(file_name):
    print(f'Чтение файла {file_name}')
    try:
        with open(file_name, encoding='utf-8') as fn:
            lines = fn.readlines()
            print(lines)
    except UnicodeDecodeError:
        print('Ошибка декодирования!')
    except Exception:
        print('Ошибка!')


if __name__ == '__main__':
    file_name = 'test_file.txt'
    lines = ['сетевое программирование', 'сокет', 'декоратор']
    file_create(file_name, lines)
    file_read(file_name)

    def_loc = locale.getpreferredencoding()
    print(f'Кодировка по-умолчанию: {def_loc}')

    file_create(file_name, lines, 'utf-8')
    file_read(file_name)
