"""
1. Реализовать обработку нескольких клиентов на сервере, используя функцию select.
Клиенты должны общаться в «общем чате»: каждое сообщение участника отправляется всем, подключенным к серверу.
"""
import argparse
import select
import socket
from time import time
from socket import *
import pickle
import log.server_log_config as slog
from log.log_request import log

logger = slog.ServerLogger(filename='log/server.log')
# logger = slog.ServerLogger(filename='log/server.log', lvl='debug')


@log
def main():
    parser = argparse.ArgumentParser(description='Client for chat messages')
    parser.add_argument('-a', action='store', dest='addr', default='0.0.0.0', help='Server IP-address')
    parser.add_argument('-p', action='store', dest='port', default='7777', help='Server port')
    args = parser.parse_args()
    s = server_socket(args.addr, int(args.port))
    server_listen(s)


@log
def server_socket(addr: str, port: int) -> socket:
    logger.log(f'=== Init Chat-Server {addr}:{port} ===', 'info')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.settimeout(0.2)
    return s


@log
def server_listen(s: socket):
    try:
        clients = []

        while True:
            logger.log('Listen...', 'debug')
            try:
                client, c_addr = s.accept()
            except timeout as e:
                logger.log('Listen timeout', 'debug')
            except Exception as e:
                logger.log(str(e), 'error')
            else:
                logger.log(f'Connected client from {c_addr}', 'info')
                clients.append(client)
            finally:
                r, w, e = [], [], []

                try:
                    r, w, e = select.select(clients, clients, [], 10)
                except Exception as e:
                    pass

                requests = server_read_requests(r, clients)
                if requests:
                    server_send_requests(w, requests, clients)

    except KeyboardInterrupt:
        logger.log('Server has down by admin', 'warning')
    except Exception as e:
        logger.log(f'Error of loop: {e}', 'critical')
    finally:
        print('Server is shutdown!')


@log
def server_read_requests(r_socks: list, clients: list) -> dict:
    requests = {}
    for sock in r_socks:
        try:
            data = sock.recv(1024)
            logger.log('Data received (' + str(len(data)) + ')', 'info')
            query = pickle.loads(data)
            # msg = server_request_processing(query)
            # send_message(sock, msg)
            requests[sock] = query
        except Exception as e:
            logger.log(f'Client {sock.fileno()} {sock.getpeername()} disconnected', 'info')
            clients.remove(sock)
    return requests


@log
def server_send_requests(w_socks: list, requests: dict, clients: list):
    for sock in w_socks:
        for writer in requests:
            try:
                send_message(sock, requests[writer])
            except Exception as e:
                logger.log(f'Client {sock.fileno()} {sock.getpeername()} disconnected', 'info')
                clients.remove(sock)


@log
def server_request_processing(query: dict) -> dict:
    available_actions = ['presence', 'msg']
    if query and 'action' in query:
        if query['action'] in available_actions:
            return get_response(200)
        else:
            return get_response(500)
    else:
        return get_response(400)


@log
def send_message(s: socket, msg: dict):
    msg = pickle.dumps(msg)
    result = s.send(msg)
    logger.log('Data sended (' + str(len(msg)) + ')', 'info')
    return result


@log
def get_response(error_code: int) -> dict:
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
