"""
Для всех функций из урока 3 написать тесты с использованием unittes / pytest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла (например, test_client.py).
"""

import unittest
from .client import *


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Подключение клиента к серверу
        """
        self.s_addr = ('localhost', 7777)
        self.sd = socket(AF_INET, SOCK_STREAM)
        self.sd.settimeout(10)
        self.sd.connect(self.s_addr)
        self.user = get_user()
        self.msg_precsence = get_presence(self.user)
        self.msg_test = 'test message'
        self.msg = get_custom_message(self.user, self.msg_test)

    def tearDown(self) -> None:
        """
        Отключение от сервера
        """
        self.sd.close()

    def test_client_presence(self):
        """
        Тестирование сообщения присутствия пользователя серверу и получения ответа от сервера
        """
        self.assertEqual(send_message(self.sd, self.msg_precsence), 104)
        query = client_recv_message(self.sd)
        self.assertIn('response', query)
        self.assertEqual(query['response'], 200)

    def test_client_custom_message(self):
        """
        Тестирование получения тестового сообщения
        """
        msg = get_custom_message(self.user, self.msg_test)
        self.assertIn('message', msg)
        self.assertEqual(msg['message'], self.msg_test)
        self.assertIn('time', msg)
        self.assertGreater(msg['time'], 0)

    def test_client_send_message(self):
        """
        Тестирование отправки сообщения
        """
        self.assertGreater(send_message(self.sd, self.msg), 90)

    def test_get_test_user(self):
        """
        Тестирование получения тестовых данных пользователя
        """
        self.assertEqual(self.user['account_name'], 'Ilusion')
        self.assertEqual(self.user['password'], '123')
        self.assertEqual(self.user['status'], 'Hey!')


if __name__ == '__main__':
    unittest.main()
