"""
Для всех функций из урока 3 написать тесты с использованием unittes / pytest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла (например, test_client.py).
"""

import unittest
from .server import *


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Запуск сервера
        """
        self.s_addr = ('0.0.0.0', 7777)
        self.sd = socket(AF_INET, SOCK_STREAM)
        self.sd.bind(self.s_addr)
        self.sd.listen(30)
        self.sd.settimeout(10)
        self.sd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # self.msg_precsence = get_presence(self.user)
        # self.msg_test = 'test message'
        # self.msg = get_custom_message(self.user, self.msg_test)

    def tearDown(self) -> None:
        """
        Отключение от сервера
        """
        self.sd.close()

    def test_server_response_codes(self):
        query = get_response(200)
        self.assertIn('alert', query)
        self.assertEqual(query['alert'], 'OK')
        self.assertEqual(get_response(400)['alert'], 'Ошибка запроса')
        self.assertEqual(get_response(500)['alert'], 'Ошибка сервера')

    def test_server_recv_message(self):
        """
        Тестирование получения запроса от клиента
        Ожидает 30 секунд, за это время нужно запустить клиента client.py
        """
        query = server_accept(self.sd)
        self.assertIn('action', query)
        self.assertEqual(query['action'], 'presence')


if __name__ == '__main__':
    unittest.main()
