"""
1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging)
    a. клиент отправляет запрос серверу;
    b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.

Функции клиента:
    - сформировать presence-сообщение;
    - отправить сообщение серверу;
    - получить ответ сервера;
    - разобрать сообщение сервера;
    - параметры командной строки скрипта client.py <addr> [<port>]:
        - addr — ip-адрес сервера;
        - port — tcp-порт на сервере, по умолчанию 7777.
"""
import argparse
from socket import *
from time import time
import pickle


def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='localhost', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()

    client_start(args.addr, int(args.port))


def client_start(addr: str, port: int):
    print(f'\n=== Init Client to Server {addr}:{port} ===\n')

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(10)
        s.connect((addr, port))

        user = get_user()
        client_scripts(s, user)

        s.close()
    except ConnectionRefusedError:
        print('Подключение не установлено')
    except Exception as e:
        print('Ошибка')


def send_message(s: socket, msg: dict):
    return s.send(pickle.dumps(msg))


def client_recv_message(s: socket):
    data = s.recv(1024)
    return pickle.loads(data)


def client_scripts(s: socket, user: dict):
    msg_precsence = get_presence(user)
    status = send_message(s, msg_precsence)
    print('Отправка: ', status)
    query = client_recv_message(s)
    check_response(query)
    msg = get_custom_message(user, 'Сообщение на отправку')
    status = send_message(s, msg)
    print('Отправка: ', status)


def check_response(query):
    if query and 'response' in query:
        print(f'Сервер ответил: {query["alert"]}')
        if query['response'] == 200:
            print('Сервер ответил что все хорошо')
        elif query['response'] == 400:
            print('Не правильно сформирован запрос')
        if query['response'] == 500:
            print('Ошибка сервера')
    else:
        print('Сервер не ответил')


def get_presence(user: dict):
    msg = {
        'action': 'presence',
        'time': time(),
        'user': {
            'account_name': user['account_name'],
            'status': user['status'],
        },
    }
    return msg


def get_custom_message(user: dict, message: str):
    msg = {
        'action': 'msg',
        'time': time(),
        'to': 'server',
        'from': user['account_name'],
        'message': message,
    }
    return msg


def get_user():
    return {
        'account_name': 'Ilusion',
        'password': '123',
        'status': 'Hey!'
    }


if __name__ == '__main__':
    main()
