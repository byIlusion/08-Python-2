import datetime
from random import choice, randint
import json


file_name = 'orders.json'
buyers = ['Вася', 'Петя', 'Афоня', 'Ваня', 'Аленушка', 'Марфа', 'Настя', 'Ксю']
items = [
    {'item': 'Ватрушка', 'price': 15.25},
    {'item': 'Плюшка', 'price': 25.00},
    {'item': 'Слойка', 'price': 18.50},
    {'item': 'Кекс', 'price': 49.99},
    {'item': 'Пончик', 'price': 78.15},
    {'item': 'Макарон', 'price': 250.00}
]


def write_order_to_json(order):
    orders = read_orders_from_json()
    orders['orders'].append(order)
    with open(file_name, 'w') as f:
        json.dump(orders, f, indent=4)
    print(f'Добавлен заказ:\n\t{order_to_str(order)}')
    print(f'\nЗаказы ({len(orders["orders"])}):')
    for o in orders['orders']:
        print(f'\t{order_to_str(o)}')



def read_orders_from_json():
    try:
        with open(file_name) as f:
            orders = json.load(f)
    except FileNotFoundError:
        print(f'Файл {file_name} не найден. Будет создан')
        orders = {"orders": []}
    except Exception:
        orders = {"orders": []}
    return orders


def order_to_str(order):
    return f'{order["item"]}, {order["quantity"]} шт. по {order["price"]} руб. ' \
           f'(ИТОГО: {order["quantity"] * order["price"]} руб.). ' \
           f'Покупатель: {order["buyer"]}'


def get_rand_order():
    order = choice(items)
    order_data = {
        'quantity': randint(1, 10),
        'buyer': choice(buyers),
        'date': datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    }
    order.update(order_data)
    return order


if __name__ == '__main__':
    order = get_rand_order()
    write_order_to_json(order)
