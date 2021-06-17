"""
2. Реализовать функции отправки/приема данных на стороне клиента.
Чтобы упростить разработку на данном этапе, пусть клиентское приложение будет либо только принимать,
либо только отправлять сообщения в общий чат. Эти функции надо реализовать в рамках отдельных скриптов.
"""
import argparse
from socket import *
from time import time
import pickle
import log.client_log_config as clog
from log.log_request import log

logger = clog.ClientLogger(filename='log/client.log')
# logger = clog.ClientLogger(filename='log/client.log', lvl='debug')


@log
def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='localhost', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()

    user_type = input('Enter a type of connection to server (r - reader, w - writer): ')
    if user_type not in ['r', 'w']:
        print('Bad enter!')
        return

    client_start((args.addr, int(args.port)), user_type)


@log
def client_start(address: tuple, user_type: str):
    logger.log(f'=== Init a Chat-Client connection to Server {address[0]}:{address[1]} ===', 'info')
    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(address)
            if user_type == 'r':
                client_reader_loop(s)
            else:
                while True:
                    user_name = input('Enter you name: ')
                    if user_name != '':
                        break
                user = get_user(user_name, user_type)
                client_writer_loop(s, user)
    except ConnectionRefusedError:
        logger.log('Connection refused', 'error')
    except KeyboardInterrupt:
        logger.log('Client closed a connection', 'info')
    except Exception as e:
        logger.log('Error', 'critical')
    finally:
        print('Good bye')


@log
def client_reader_loop(s: socket):
    while True:
        try:
            query = client_recv_message(s)
            client_request_processing(query)
        except timeout:
            logger.log('Timeout...')


@log
def client_writer_loop(s: socket, user: dict):
    while True:
        msg = input('Enter a message for all users (q - quit):\n')
        if msg == 'q':
            break
        try:
            msg = get_custom_message(user, msg)
            client_send_message(s, msg)
        except Exception as e:
            logger.log('Error a sending message', 'error')


@log
def client_send_message(s: socket, msg: dict):
    msg = pickle.dumps(msg)
    result = s.send(msg)
    logger.log('Data sended (' + str(len(msg)) + ')', 'info')
    return result


@log
def client_recv_message(s: socket):
    data = s.recv(1024)
    logger.log('Data received (' + str(len(data)) + ')', 'info')
    return pickle.loads(data)


@log
def client_request_processing(query):
    available_actions = ['msg']
    if query and 'action' in query and query['action'] in available_actions:
        user_from = query['from'] if 'from' in query else 'Anonimous'
        msg = query['msg'] if 'msg' in query else ''
        print(f'{user_from}: {msg}')
    else:
        pass


@log
def client_scripts(s: socket, user: dict):
    msg_presence = get_presence(user)
    client_send_message(s, msg_presence)
    query = client_recv_message(s)
    check_response(query)
    msg = get_custom_message(user, 'Сообщение на отправку')
    client_send_message(s, msg)


@log
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


@log
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


@log
def get_custom_message(user: dict, message: str):
    msg = {
        'action': 'msg',
        'time': time(),
        'to': 'server',
        'from': user['account_name'],
        'msg': message,
    }
    return msg


@log
def get_user(user_name: str = 'Ilusion', user_type: str = ''):
    return {
        'account_name': user_name,
        'password': '123',
        'status': 'Hey!',
        'user_type': user_type
    }


if __name__ == '__main__':
    main()
