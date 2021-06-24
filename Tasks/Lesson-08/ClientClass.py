"""
1. На клиентской стороне реализовать прием и отправку сообщений с помощью потоков в P2P-формате
    (обмен сообщениями между двумя пользователями).
    Реализовать клиента с помощью потоков.
    Один поток - принимает сообщения, второй - держит инпут и их отправляет

2. сделать возможность отправки нескольких типов сообщений:
    presence, вступление/выход из конференции, отправка сообщения онлайн клиенту
"""
import argparse
from socket import *
from threading import Thread
from time import time, sleep
import pickle

import log.client_log_config as clog
from log.log_request import log


class Client:
    _chats: list = []
    _users: list = []

    user: dict = {}

    _addr: tuple
    _sock: socket


    @log
    def __init__(self, addr: tuple = ("0.0.0.0", 7777)):
        self._logger = clog.ClientLogger(filename='log/client.log')
        # self._logger = clog.ClientLogger(filename='log/client.log', lvl='debug')
        self._logger.log(f'=== Init a Chat-Client connection to Server {addr[0]}:{addr[1]} ===', 'info')

        self._addr = addr

    @log
    def start(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as self._sock:
                self._sock.settimeout(3)
                self._sock.connect(self._addr)
                self.user_set()

                self._presence()

                t_r = Thread(target=self.reader_loop)
                t_r.daemon = True
                t_r.start()

                t_w = Thread(target=self.writer_loop)
                t_w.daemon = True
                t_w.start()
                t_w.join()
        except ConnectionRefusedError:
            self._logger.log('Connection refused', 'error')
            print('Server not started')
        except KeyboardInterrupt:
            self._logger.log('Client closed a connection', 'info')
        except Exception as e:
            self._logger.log(f'Error: {e}', 'critical')
        finally:
            self.stop()
            print('Good bye')

    @log
    def stop(self):
        self._sock.close()

    @log
    def reader_loop(self):
        try:
            while True:
                request = self._read()
                self.request_processing(request)
        except Exception as e:
            pass

    @log
    def writer_loop(self):
        try:
            while True:
                msg = self.message()
                self._send(msg)
        except Exception as e:
            self._logger.log(e, 'info')

    @log
    def _read(self):
        try:
            data = self._sock.recv(1024)
            self._logger.log(f'Data received ({str(len(data))})', 'info')
            return pickle.loads(data)
        except timeout:
            self._logger.log('Timeout...', 'debug')

    @log
    def _send(self, msg: dict) -> bool:
        try:
            result = self._sock.send(pickle.dumps(msg))
            self._logger.log(f'Data sended ({str(len(msg))})', 'info')
            return bool(result)
        except Exception as e:
            self._logger.log('Error a sending message', 'error')

    @log
    def request_processing(self, request: dict):
        available_actions = ['msg']
        if request and 'action' in request and request['action'] in available_actions:
            user_from = request['from'] if 'from' in request else 'Anonymous'
            msg = request['msg'] if 'msg' in request else ''
            print(f'{user_from}: {msg}')
        else:
            pass

    @log
    def _presence(self):
        msg = self.message('presence')
        result = self._send(msg)
        request = self._read()
        if request:
            self._users = request['users'] if 'users' in request else []
            self._chats = request['chats'] if 'chats' in request else []
        self._logger.log('Presence completed')
        return result

    @log
    def user_set(self):
        while True:
            user_name = input('Enter you name: ')
            if user_name != '':
                break
        self.user = {
            'account_name': user_name,
            'status': 'Hey!',
        }

    @log
    def message(self, msg_type: str = 'msg') -> dict:
        msg = {
            'action': msg_type,
            'time': time(),
            'from': self.user['account_name'],
        }

        if msg_type == 'msg':
            message = input('Enter a message for all users (q - quit):\n')
            if message == 'q':
                raise Exception('Quit')
            msg.update({
                'to': '#all',
                'msg': message,
            })

        elif msg_type == 'presence':
            msg.update({
                'user': self.user,
            })

        return msg


@log
def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='localhost', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()

    c = Client((args.addr, int(args.port)))
    c.start()


if __name__ == '__main__':
    main()
