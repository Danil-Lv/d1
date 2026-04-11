from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, Field
from wtforms.validators import DataRequired, Email, Optional, ValidationError
import unittest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['WTF_CSRF_ENABLED'] = False  # Важно для тестов

# --- ВАЛИДАТОРЫ (Задача 2) ---

class NumberLength:
    def __init__(self, min_len: int, max_len: int, message: str = None):
        self.min = min_len
        self.max = max_len
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        data_str = str(field.data) if field.data is not None else ""
        if not (self.min <= len(data_str) <= self.max):
            err_msg = self.message or f"Число должно быть от {self.min} до {self.max} знаков."
            raise ValidationError(err_msg)

def number_length_func(min_len: int, max_len: int, message: str = None):
    def _number_length(form: FlaskForm, field: Field):
        data_str = str(field.data) if field.data is not None else ""
        if not (min_len <= len(data_str) <= max_len):
            err_msg = message or f"Длина числа должна быть от {min_len} до {max_len} символов."
            raise ValidationError(err_msg)
    return _number_length

# --- ФОРМА (Задача 1) ---

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[
        DataRequired(),
        NumberLength(min_len=10, max_len=10) # Используем наш класс
    ])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    index = IntegerField('Index', validators=[
        DataRequired(),
        number_length_func(min_len=5, max_len=6) # Используем нашу функцию
    ])
    comment = TextAreaField('Comment', validators=[Optional()])

# --- ЭНДПОИНТ ---

@app.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()
    form = RegistrationForm(data=data)

    if form.validate():
        return jsonify({"message": "Регистрация прошла успешно!"}), 200
    else:
        return jsonify({"errors": form.errors}), 400

# --- ТЕСТЫ (Задача 3) ---

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_registration_success(self):
        """Успешная регистрация"""
        data = {
            "email": "test@mail.ru",
            "phone": 1234567890,
            "name": "Ivan",
            "address": "Msk",
            "index": 123456
        }
        response = self.client.post('/registration', json=data)
        self.assertEqual(response.status_code, 200)

    def test_phone_invalid_length(self):
        """Ошибка: телефон короче 10 цифр"""
        data = {"email": "t@t.ru", "phone": 123, "name": "X", "address": "X", "index": 12345}
        response = self.client.post('/registration', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.get_json()['errors'])

    def test_email_invalid_format(self):
        """Ошибка: неверный формат почты"""
        data = {"email": "bad-email", "phone": 1234567890, "name": "X", "address": "X", "index": 12345}
        response = self.client.post('/registration', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.get_json()['errors'])

if __name__ == '__main__':
    # Если запустить файл напрямую, запустятся тесты
    unittest.main()
