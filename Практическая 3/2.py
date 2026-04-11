import unittest
from Практическая_2.decrypt import decrypt

class TestDecryptor(unittest.TestCase):
    def test_logic_grouping(self):
        # Группа 1: Базовые случаи и одна точка
        with self.subTest(group="Base cases"):
            self.assertEqual(decrypt("абра-кадабра."), "абра-кадабра")
            self.assertEqual(decrypt("."), "")

        # Группа 2: Несколько точек (удаление нескольких символов)
        with self.subTest(group="Multiple dots"):
            self.assertEqual(decrypt("абраа..-кадабра"), "абра-кадабра")
            self.assertEqual(decrypt("абраа..-.кадабра"), "абра-кадабра")
            self.assertEqual(decrypt("абра--..кадабра"), "абра-кадабра")
            self.assertEqual(decrypt("абрау...-кадабра"), "абра-кадабра")
            self.assertEqual(decrypt("1..2.3"), "23")

        # Группа 3: Избыточное количество точек
        with self.subTest(group="Excessive dots"):
            self.assertEqual(decrypt("абра........"), "")
            self.assertEqual(decrypt("1......................."), "")
            self.assertEqual(decrypt("абр......a."), "a")

if __name__ == '__main__':
    unittest.main()
