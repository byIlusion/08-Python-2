"""
Для всех функций из урока 3 написать тесты с использованием unittes / pytest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла (например, test_client.py).
"""

import unittest
from ServerClass import *


class TestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Запуск сервера
        """
        self.server = Server()

    def tearDown(self) -> None:
        """
        Отключение от сервера
        """
        self.server.stop()

    def test_get_response(self):
        """
        Тестирование получения ответов ина основании кодов
        """
        query = self.server.get_response(200)
        self.assertIn('alert', query)
        self.assertEqual(query['alert'], 'OK')
        self.assertEqual(self.server.get_response(400)['alert'], 'Ошибка запроса')
        self.assertEqual(self.server.get_response(500)['alert'], 'Ошибка сервера')


if __name__ == '__main__':
    unittest.main()
