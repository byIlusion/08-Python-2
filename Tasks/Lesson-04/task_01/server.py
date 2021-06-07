"""
1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging)
    a. клиент отправляет запрос серверу;
    b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.

Функции сервера:
    - принимает сообщение клиента;
    - формирует ответ клиенту;
    - отправляет ответ клиенту;
    - имеет параметры командной строки:
        - -p <port> — TCP-порт для работы (по умолчанию использует 7777);
        - -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
import argparse
import socket
from time import time
from socket import *
import pickle


def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='0.0.0.0', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()
    server_start(args.addr, int(args.port))


def server_start(addr: str, port: int):
    print(f'\n=== Init Server {addr}:{port} ===\n')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.settimeout(5)

    server_listen(s)


def server_listen(s: socket):
    while True:
        print('listen')
        query = server_accept(s)
        print(query)


def server_accept(s: socket):
    try:
        client, c_addr = s.accept()
        print(f'Connected client from {c_addr}')
        data = client.recv(1024)
        query = pickle.loads(data)
        print(query)
        if query and 'action' in query:
            if query['action'] == 'presence':
                msg = get_response(200)
                send_message(client, msg)
            else:
                msg = get_response(500)
                send_message(client, msg)
        else:
            msg = get_response(400)
            send_message(client, msg)
        client.close()
        return query
    except Exception as e:
        pass


def send_message(s: socket, msg: dict):
    return s.send(pickle.dumps(msg))


def get_response(error_code: int):
    errors = {
        200: 'OK',
        400: 'Ошибка запроса',
        500: 'Ошибка сервера',
    }
    msg = {
        'response': error_code,
        'alert': errors[error_code]
    }
    return msg


if __name__ == '__main__':
    main()
