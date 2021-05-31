
def str_to_bytes(word):
    try:
        bytes_word = str(word).encode('utf-8')
        return bytes_word
    except UnicodeEncodeError:
        print(f'Слово «{word}» не возможно преобразовать в битовый тип')


def bytes_to_str(bytes_word):
    try:
        word = bytes_word.decode('utf-8')
        return word
    except AttributeError:
        print('Данный тип переменной не имеет метода decode()')
    except Exception:
        print('Ошибка декодирования')


if __name__ == '__main__':
    words = ['разработка', 'администрирование', 'protocol', 'standard']
    for word in words:
        bytes_word = str_to_bytes(word)
        str_word = bytes_to_str(bytes_word)
        print(f'{word} => {bytes_word} => {str_word}')
