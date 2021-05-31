
def convert_to_bytes(word):
    return bytes(word, 'ascii')


if __name__ == '__main__':
    words = ['class', 'function', 'method']
    for word in words:
        bytes_word = convert_to_bytes(word)
        print(f'Значение: {bytes_word}\n\tТип: {type(bytes_word)}\n\tДлина строки: {len(bytes_word)}')
