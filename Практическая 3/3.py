import unittest
from Практическая_2.seven import app, storage

class TestFinanceApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        storage.clear()  # Очищаем данные перед каждым тестом
        # Предзаполняем данными
        storage.update({
            2023: {1: 100, 2: 200},
            2024: {5: 500}
        })

    # --- ТЕСТЫ ДЛЯ /add/ ---

    def test_add_correct(self):
        """Успешное добавление траты"""
        response = self.client.get('/add/20230110/50')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage[2023][1], 150)  # 100 было + 50 добавили

    def test_add_new_month(self):
        """Добавление в новый месяц"""
        self.client.get('/add/20230315/300')
        self.assertEqual(storage[2023][3], 300)

    def test_add_wrong_date_format(self):
        """Проверка падения при некорректной дате (буквы или короткая строка)"""
        # По условию нужно добиться, чтобы эндпоинт 'свалился'
        with self.assertRaises(ValueError):
            # int('abcd') вызовет ValueError
            self.client.get('/add/yearmonthday/100')

    # --- ТЕСТЫ ДЛЯ /calculate/ (Год) ---

    def test_calculate_year_success(self):
        """Расчет за существующий год"""
        response = self.client.get('/calculate/2023')
        self.assertIn("300", response.data.decode()) # 100 + 200

    def test_calculate_year_not_found(self):
        """Расчет за год, которого нет в базе"""
        response = self.client.get('/calculate/2020')
        self.assertEqual(response.status_code, 404)

    def test_calculate_year_empty_storage(self):
        """Расчет года при пустом хранилище"""
        storage.clear()
        response = self.client.get('/calculate/2023')
        self.assertEqual(response.status_code, 404)

    # --- ТЕСТЫ ДЛЯ /calculate/ (Месяц) ---

    def test_calculate_month_success(self):
        """Расчет за существующий месяц"""
        response = self.client.get('/calculate/2023/1')
        self.assertIn("100", response.data.decode())

    def test_calculate_month_not_found(self):
        """Расчет за несуществующий месяц"""
        response = self.client.get('/calculate/2023/12')
        self.assertEqual(response.status_code, 404)

    def test_calculate_month_leading_zero(self):
        """Проверка корректности отображения месяца (01.2023)"""
        response = self.client.get('/calculate/2023/1')
        self.assertIn("01.2023", response.data.decode())

if __name__ == '__main__':
    unittest.main()
