import unittest
import datetime
from person import Person

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("Иван", 1990, "Москва")

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        expected_age = current_year - 1990
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Иван")

    def test_set_name(self):
        self.person.set_name("Пётр")
        self.assertEqual(self.person.get_name(), "Пётр")

    def test_set_address(self):
        self.person.set_address("Питер")
        self.assertEqual(self.person.get_address(), "Питер")

    def test_is_homeless_false(self):
        self.assertFalse(self.person.is_homeless())

    def test_is_homeless_true(self):
        homeless_person = Person("Никто", 2000, address='')
        self.assertTrue(homeless_person.is_homeless())

if __name__ == '__main__':
    unittest.main()
