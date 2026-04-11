import sys
import traceback
import unittest
from io import StringIO


class Redirect:
    def __init__(self, *, stdout=None, stderr=None):
        """
        Используем *, чтобы аргументы были строго именованными (непозиционными).
        """
        self._stdout_target = stdout
        self._stderr_target = stderr
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        # Сохраняем текущие потоки (поддержка вложенности)
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr

        # Перенаправляем, если переданы объекты
        if self._stdout_target is not None:
            sys.stdout = self._stdout_target
        if self._stderr_target is not None:
            sys.stderr = self._stderr_target

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Если возникло исключение и stderr перенаправлен
        if exc_type is not None and self._stderr_target is not None:
            # Записываем traceback в текущий sys.stderr (который уже наш target)
            traceback.print_exception(exc_type, exc_val, exc_tb, file=sys.stderr)

        # Возвращаем старые потоки на место
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

        # Возвращаем True, чтобы исключение не "прокидывалось" дальше и не дублировалось в консоль,
        # если мы его уже записали в файл (согласно логике примера).
        return True


# --- ТЕСТЫ ---

class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        """Проверка перенаправления только stdout"""
        out = StringIO()
        with Redirect(stdout=out):
            print("Hello Test")
        self.assertEqual(out.getvalue().strip(), "Hello Test")

    def test_redirect_stderr(self):
        """Проверка перенаправления только stderr (исключение)"""
        err = StringIO()
        with Redirect(stderr=err):
            raise ValueError("Test Error")
        self.assertIn("ValueError: Test Error", err.getvalue())

    def test_no_args(self):
        """Проверка работы без аргументов (ничего не ломается)"""
        with Redirect():
            print("Normal print")
        # Если не упало — успех

    def test_nested_redirect(self):
        """Проверка вложенности (сохранение текущих потоков)"""
        out1 = StringIO()
        out2 = StringIO()
        with Redirect(stdout=out1):
            print("Level 1")
            with Redirect(stdout=out2):
                print("Level 2")
            print("Back to Level 1")

        self.assertIn("Level 1\nBack to Level 1", out1.getvalue())
        self.assertIn("Level 2", out2.getvalue())


if __name__ == '__main__':
    # Рекомендуемый способ запуска тестов для избежания конфликтов потоков
    with open('test_results.txt', 'w') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
