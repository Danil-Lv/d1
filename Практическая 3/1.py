import unittest
from freezegun import freeze_time
from Практическая_2.app import app



class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @freeze_time("2024-05-20")  # Monday (Male gender: "Хорошего")
    def test_can_get_correct_weekday_monday(self):
        username = "Ivan"
        response = self.app.get(f'/hello-world/{username}')
        response_text = response.data.decode('utf-8')

        # Check if the weekday is correct and matches the "frozen" time
        self.assertIn("понедельника", response_text)
        self.assertIn("Хорошего", response_text)

    @freeze_time("2024-05-22")  # Wednesday (Female gender: "Хорошей")
    def test_can_get_correct_weekday_wednesday(self):
        username = "Anna"
        response = self.app.get(f'/hello-world/{username}')
        response_text = response.data.decode('utf-8')

        self.assertIn("среды", response_text)
        self.assertIn("Хорошей", response_text)

    @freeze_time("2024-05-23")  # Thursday
    def test_username_with_wish_phrase(self):
        # Specific task requirement: username is 'Хорошей среды'
        username = "Хорошей среды"
        response = self.app.get(f'/hello-world/{username}')
        response_text = response.data.decode('utf-8')

        # We check that the 'name' is printed correctly as given,
        # but the actual day is Thursday (the frozen date)
        self.assertIn(f"Привет, {username}", response_text)
        self.assertIn("четверга", response_text)


if __name__ == '__main__':
    unittest.main()
