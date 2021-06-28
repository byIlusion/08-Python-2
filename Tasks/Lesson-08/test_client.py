"""
Для всех функций из урока 3 написать тесты с использованием unittes / pytest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла (например, test_client.py).
"""

import unittest
from ClientClass import *


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Подключение клиента к серверу
        """
        self.client = Client()

    # def tearDown(self) -> None:
    #     """
    #     Отключение от сервера
    #     """
    #     self.client.stop()

    def test_request_processing(self):
        """
        Тестирование сообщения присутствия пользователя серверу и получения ответа от сервера
        """
        query = {
            'action': 'msg',
            'from': 'tester',
            'msg': 'test'
        }
        self.assertEqual(self.client.request_processing(query), None)


if __name__ == '__main__':
    unittest.main()
