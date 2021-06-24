import argparse
import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
import pickle
import log.server_log_config as slog
from log.log_request import log


class Server:
    _users = {}
    _chats = ["Main chat"]
    _clients = []

    @log
    def __init__(self, addr: tuple = ("0.0.0.0", 7777)):
        self._logger = slog.ServerLogger(filename="log/server.log")
        # self._logger = slog.ServerLogger(filename="log/server.log", consoled=True)
        self._logger.log(f"=== Init Chat-Server {addr[0]}:{addr[1]} ===", "info")

        self._addr = addr
        self._socket_init()

    @log
    def _socket_init(self):
        self._s = socket(AF_INET, SOCK_STREAM)
        self._s.bind(self._addr)
        self._s.listen(5)
        self._s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._s.settimeout(0.2)

    @log
    def start(self):
        try:
            while True:
                self._logger.log("Listen...", "debug")
                try:
                    client, c_addr = self._s.accept()
                except timeout as e:
                    self._logger.log("Listen timeout", "debug")
                except Exception as e:
                    self._logger.log(str(e), "error")
                else:
                    self._logger.log(f"Connected client from {c_addr}", "info")
                    self._clients.append(client)
                finally:
                    r, w, e = [], [], []

                    try:
                        r, w, e = select.select(self._clients, self._clients, [], 10)
                    except Exception as e:
                        pass

                    requests = self._read(r)
                    if requests:
                        self._send(w, requests)

        except KeyboardInterrupt:
            self._logger.log("Server has down by admin", "warning")
        except Exception as e:
            self._logger.log(f"Error of loop: {e}", "critical")
        finally:
            self.stop()
            self._logger.log(f"Server is shutdown", "info")

    @log
    def stop(self):
        self._s.close()

    @log
    def client_remove(self, client) -> dict:
        user = self._users.pop(client)
        self._clients.remove(client)
        self._logger.log(f"Client {user['account_name']} ({client.fileno()} {client.getpeername()}) disconnected", "info")
        return user

    @log
    def _read(self, r_socks: list) -> list:
        requests = []
        for sock in r_socks:
            try:
                data = sock.recv(1024)
                self._logger.log(f"Data received ({str(len(data))})", "info")
                query = pickle.loads(data)

                requests.append(self.request_processing(sock, query))
            except Exception as e:
                self.client_remove(sock)

        return requests

    @log
    def _send(self, w_socks: list, requests: list):
        for request in requests:
            socks = request["to"].copy()
            for sock in socks:
                request["to"] = self._users[sock]["account_name"]
                if sock in w_socks:
                    try:
                        msg = pickle.dumps(request)
                        sock.send(msg)
                        self._logger.log(f"Data sent ({str(len(msg))})", "info")
                    except Exception as e:
                        self.client_remove(sock)

    @log
    def request_processing(self, sock: socket, query: dict) -> dict:
        available_actions = ["presence", "msg"]
        if query and "action" in query:
            if query["action"] in available_actions:
                request = self.get_response(200)

                if query["action"] == "presence":
                    request["to"] = [sock]
                    self._users[sock] = query["user"]
                    self._logger.log(f"User {query['user']['account_name']} connected")

                elif query["action"] == "msg":
                    request["action"] = "msg"
                    request["from"] = query["from"]
                    request["msg"] = query["msg"]
                    if query["to"] == "#all":
                        request["to"] = list(self._users.keys())
                    else:
                        request["to"] = []
                        for s, u in enumerate(self._users):
                            if u["account_name"] == query["to"]:
                                request["to"].append(s)

                request.update({
                    "chats": self._chats,
                    "users": list(self._users.values()),
                })

                return request
            else:
                return self.get_response(500)
        else:
            return self.get_response(400)

    @log
    def get_response(self, error_code: int) -> dict:
        errors = {
            200: "OK",
            400: "Ошибка запроса",
            500: "Ошибка сервера",
        }
        msg = {
            "response": error_code,
            "alert": errors[error_code]
        }
        return msg


@log
def main():
    parser = argparse.ArgumentParser(description="Client for chat messages")
    parser.add_argument("-a", action="store", dest="addr", default="0.0.0.0", help="Server IP-address")
    parser.add_argument("-p", action="store", dest="port", default="7777", help="Server port")
    args = parser.parse_args()

    s = Server((args.addr, int(args.port)))
    s.start()


if __name__ == "__main__":
    main()
