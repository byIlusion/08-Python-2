
def convert_to_bytes(word):
    try:
        bytes_word = bytes(word, 'ascii')
        return bytes_word
    except UnicodeEncodeError:
        print(f'Слово «{word}» не возможно преобразовать в битовый тип')


if __name__ == '__main__':
    words = ['attribute', 'класс', 'функция', 'type']
    for word in words:
        bytes_word = convert_to_bytes(word)
        if bytes_word:
            print(f'Значение: {bytes_word}\n\tТип: {type(bytes_word)}\n\tДлина строки: {len(bytes_word)}')
