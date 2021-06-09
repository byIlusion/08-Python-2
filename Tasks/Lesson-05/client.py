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
from socket import *
from time import time
import pickle
import log.client_log_config as clog

logger = clog.ClientLogger(filename='log/client.log')


def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='localhost', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()

    client_start(args.addr, int(args.port))


def client_start(addr: str, port: int):
    logger.log(f'=== Init Clients connection to Server {addr}:{port} ===', 'info')
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(10)
        s.connect((addr, port))

        user = get_user()
        client_scripts(s, user)

        s.close()
    except ConnectionRefusedError:
        logger.log('Connection refused', 'error')
    except Exception as e:
        print('Ошибка')
        logger.log('Error', 'critical')


def send_message(s: socket, msg: dict):
    msg = pickle.dumps(msg)
    result = s.send(msg)
    logger.log('Data sended (' + str(len(msg)) + ')', 'info')
    return result


def client_recv_message(s: socket):
    data = s.recv(1024)
    logger.log('Data received (' + str(len(data)) + ')', 'info')
    return pickle.loads(data)


def client_scripts(s: socket, user: dict):
    msg_precsence = get_presence(user)
    send_message(s, msg_precsence)
    query = client_recv_message(s)
    check_response(query)
    msg = get_custom_message(user, 'Сообщение на отправку')
    send_message(s, msg)


def check_response(query):
    if query and 'response' in query:
        lvl = 'info'
        alert = query["alert"] if query["alert"] else '-'
        if query['response'] == 400:
            lvl = 'warning'
        elif query['response'] == 500:
            lvl = 'error'
        logger.log(f'Code: ({query["response"]}), Server response: {alert}', lvl)
    else:
        logger.log('Server did`t respond', 'error')


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
