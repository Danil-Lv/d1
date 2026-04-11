import unittest


class BlockErrors:
    def __init__(self, err_types):
        # Принимаем набор типов ошибок (set или tuple)
        self.err_types = err_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Если исключения не было, просто выходим
        if exc_type is None:
            return True

        # Проверяем, есть ли тип исключения (или его родитель) в разрешенном списке
        # isinstance(exc_val, tuple(self.err_types)) корректно обработает иерархию
        if any(issubclass(exc_type, err) for err in self.err_types):
            return True  # Игнорируем ошибку

        # Если ошибка не в списке, возвращаем False (она прокидывается выше)
        return False


# --- ТЕСТЫ ---

class TestBlockErrors(unittest.TestCase):

    def test_ignore_error(self):
        """1. Ошибка игнорируется (Пример 1)"""
        try:
            err_types = {ZeroDivisionError, TypeError}
            with BlockErrors(err_types):
                a = 1 / 0
            executed = True
        except ZeroDivisionError:
            executed = False
        self.assertTrue(executed)

    def test_raise_error_up(self):
        """2. Ошибка прокидывается выше (Пример 2)"""
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_blocks(self):
        """3. Ошибка прокидывается во внутреннем и игнорируется во внешнем (Пример 3)"""
        outer_err_types = {TypeError}
        inner_err_types = {ZeroDivisionError}

        # Мы ожидаем, что внешний блок поймает TypeError,
        # который пролетит сквозь внутренний
        try:
            with BlockErrors(outer_err_types):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
                # Эта строка не должна выполниться
                self.fail("Внутренний блок не должен был завершиться успешно")
            executed_outer = True
        except TypeError:
            executed_outer = False

        self.assertTrue(executed_outer)

    def test_child_errors_ignore(self):
        """4. Дочерние ошибки игнорируются (Пример 4)"""
        # ArithmeticError — родитель для ZeroDivisionError
        err_types = {ArithmeticError}
        try:
            with BlockErrors(err_types):
                a = 1 / 0
            executed = True
        except ZeroDivisionError:
            executed = False
        self.assertTrue(executed)

    def test_exception_base_class(self):
        """Дополнительно: проверка с базовым классом Exception"""
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'
        # Если не упало — успех


if __name__ == '__main__':
    unittest.main()
