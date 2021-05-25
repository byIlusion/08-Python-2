
def variable_output(word):
    """Вывод """
    print(word, type(word))


if __name__ == '__main__':
    words = ['разработка', 'сокет', 'декоратор']
    for word in words:
        variable_output(word)

    words_unicode = [
        '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
        '\u0441\u043e\u043a\u0435\u0442',
        '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
    ]
    for word in words_unicode:
        variable_output(word)
