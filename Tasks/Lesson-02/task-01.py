import re
import csv


def get_data():
    names_files = ['info_1', 'info_2', 'info_3']
    main_data = {
        'os_prod_list': {'title': 'Изготовитель системы', 'data': []},
        'os_name_list': {'title': 'Название ОС', 'data': []},
        'os_code_list': {'title': 'Код продукта', 'data': []},
        'os_type_list': {'title': 'Тип системы', 'data': []},
    }
    for file_name in names_files:
        lines = readlines_gen(file_name + '.txt')
        for line in lines:
            for key, value in main_data.items():
                if re.match(value['title'], line):
                    main_data[key]['data'].append(parse_data(line))
    return main_data


def write_to_csv(f):
    data = get_data()
    csv_data = [[]]
    for i, column in enumerate(data):
        csv_data[0].append(data[column]['title'])
        for j, row in enumerate(data[column]['data']):
            if len(csv_data) < len(data[column]['data']):
                for _ in range(len(data[column]['data'])):
                    csv_data.append([])
            csv_data[j + 1].append(data[column]['data'][j])
    writer = csv.writer(f, delimiter=';')
    writer.writerows(csv_data)


def readlines_gen(file_name):
    with open(file_name) as f:
        for line in f.readlines():
            yield line


def parse_data(line: str):
    data = line.split(':')
    if len(data) == 2:
        return data[1].strip()
    else:
        return data[0].strip()


if __name__ == '__main__':
    with open('info.csv', 'w') as f:
        write_to_csv(f)
