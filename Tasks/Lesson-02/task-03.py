import yaml


file_name = 'file.yaml'
example_dict = {
    'list': ['string', 1, True],
    'integer': 15,
    'chars': {
        '\u00A9': '©',
        '\u00AB': '«',
        '\u00BB': '»',
    }
}


def write_to_yaml(data):
    with open(file_name, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    print(f'Данные сохранены в файл {file_name}')


def read_from_yaml():
    data = None
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception:
        print('Не удалось открыть файл')
    return data


if __name__ == '__main__':
    write_to_yaml(example_dict)
    print(f'Сохраненные данные:\n\t{example_dict}')
    data = read_from_yaml()
    print(f'Данные из файла {file_name}:\n\t{data}')
    print('Данные равны' if example_dict == data else 'Данные различаются')
