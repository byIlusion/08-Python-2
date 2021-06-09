"""
1. В директории проекта создать каталог log, в котором для клиентской и серверной сторон
в отдельных модулях формата client_log_config.py и server_log_config.py создать логгеры;

2. В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
    - Создание именованного логгера;
    - Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
    - Журналирование должно производиться в лог-файл;
    - На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.

3. Реализовать применение созданных логгеров для решения двух задач:
    - Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование
      и обеспечить вывод служебных сообщений в лог-файл;
    - Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.
"""
import argparse
import socket
from time import time
from socket import *
import pickle
import log.server_log_config as slog

logger = slog.ServerLogger(filename='log/server.log')


def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='0.0.0.0', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()
    server_start(args.addr, int(args.port))


def server_start(addr: str, port: int):
    logger.log(f'=== Init Server {addr}:{port} ===', 'info')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.settimeout(5)

    server_listen(s)


def server_listen(s: socket):
    try:
        while True:
            logger.log('Listen...', 'info')
            server_accept(s)
    except KeyboardInterrupt:
        logger.log('Server has down by admin', 'warning')
    except Exception as e:
        logger.log(f'Error of loop: {e}', 'critical')


def server_accept(s: socket):
    try:
        client, c_addr = s.accept()
        if client:
            logger.log(f'Connected client from {c_addr}', 'info')
            query = server_recv_data(client)
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
            logger.log(f'Connection with client closed', 'info')
    except timeout as e:
        logger.log('Listen timeout', 'warning')
    except Exception as e:
        logger.log(e, 'error')


def server_recv_data(s: socket):
    data = s.recv(1024)
    logger.log('Data received (' + str(len(data)) + ')', 'info')
    return pickle.loads(data)


def send_message(s: socket, msg: dict):
    msg = pickle.dumps(msg)
    result = s.send(msg)
    logger.log('Data sended (' + str(len(msg)) + ')', 'info')
    return result


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
