import subprocess
import shlex
import unittest
from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['WTF_CSRF_ENABLED'] = False


# --- ФОРМА ---
class CodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    timeout = IntegerField('timeout', validators=[
        DataRequired(),
        NumberRange(min=1, max=30)
    ])


# --- ЭНДПОИНТ ---
@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()
    form = CodeForm(data=data)

    if form.validate():
        code = form.code.data
        timeout = form.timeout.data

        # БЕЗОПАСНОСТЬ: Мы передаем код как отдельный аргумент в списке.
        # Это гарантирует, что даже если в коде есть ";", система не выполнит вторую команду.
        command = ["python3", "-c", code]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False  # Явно указываем False (защита от shell injection)
            )

            stdout, stderr = process.communicate(timeout=timeout)

            return jsonify({
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": process.returncode
            }), 200

        except subprocess.TimeoutExpired:
            process.kill()
            return jsonify({"error": "Исполнение кода не уложилось в данное время"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"errors": form.errors}), 400


# --- ТЕСТЫ ---
class TestRemoteExec(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_timeout_exceeded(self):
        """1. Тест на превышение тайм-аута"""
        data = {"code": "import time; time.sleep(2)", "timeout": 1}
        response = self.client.post('/run_code', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Исполнение кода не уложилось в данное время", response.get_json()['error'])

    def test_invalid_form_data(self):
        """2. Тест на некорректные данные (timeout > 30)"""
        data = {"code": "print(1)", "timeout": 35}
        response = self.client.post('/run_code', json=data)
        self.assertEqual(response.status_code, 400)

    def test_security_shell_injection(self):
        """3. Тест на защиту от Shell Injection (проверка shell=False)"""
        # Попытка закрыть кавычку и выполнить системную команду echo
        # Если бы shell=True, мы бы увидели "hacked" в ответе
        data = {
            "code": 'print("safe"); echo "hacked"',
            "timeout": 5
        }
        response = self.client.post('/run_code', json=data)

        # В безопасном режиме python попытается исполнить 'echo "hacked"' как свой код
        # и выдаст ошибку синтаксиса, а не напечатает "hacked"
        output = response.get_json().get('stdout', '')
        self.assertNotIn("hacked", output)


if __name__ == '__main__':
    # Сначала прогоняем тесты. Если всё OK — запускаем сервер.
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRemoteExec)
    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        app.run(debug=True, port=5002)
