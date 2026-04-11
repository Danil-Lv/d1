from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, Field
from wtforms.validators import DataRequired, Email, Optional, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'


# --- ЗАДАЧА 2: СОЗДАНИЕ ВАЛИДАТОРОВ ---

# 1. Валидатор на основе КЛАССА
class NumberLength:
    def __init__(self, min_len: int, max_len: int, message: str = None):
        self.min = min_len
        self.max = max_len
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        # Считаем количество цифр в числе
        data_str = str(field.data) if field.data is not None else ""
        if not (self.min <= len(data_str) <= self.max):
            # Если свое сообщение не пришло, формируем стандартное
            err_msg = self.message or f"Число должно быть от {self.min} до {self.max} знаков."
            raise ValidationError(err_msg)


# 2. Валидатор на основе ФУНКЦИИ
def number_length_func(min_len: int, max_len: int, message: str = None):
    def _number_length(form: FlaskForm, field: Field):
        data_str = str(field.data) if field.data is not None else ""
        if not (min_len <= len(data_str) <= max_len):
            err_msg = message or f"Длина числа должна быть от {min_len} до {max_len} символов."
            raise ValidationError(err_msg)

    return _number_length


# --- ЗАДАЧА 1: ПРИМЕНЕНИЕ ВАЛИДАТОРОВ В ФОРМЕ ---

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email обязателен"),
        Email(message="Неверный формат почты")
    ])

    # Используем наш КЛАССОВЫЙ валидатор для телефона
    phone = IntegerField('Phone', validators=[
        DataRequired(message="Телефон обязателен"),
        NumberLength(min_len=10, max_len=10, message="Введите ровно 10 цифр")
    ])

    name = StringField('Name', validators=[DataRequired(message="Имя обязательно")])
    address = StringField('Address', validators=[DataRequired(message="Адрес обязателен")])

    # Используем наш ФУНКЦИОНАЛЬНЫЙ валидатор для индекса
    index = IntegerField('Index', validators=[
        DataRequired(message="Индекс обязателен"),
        number_length_func(min_len=5, max_len=6, message="Индекс должен быть 5-6 цифр")
    ])

    comment = TextAreaField('Comment', validators=[Optional()])


@app.route('/registration', methods=['POST'])
def registration():
    # Получаем данные из JSON (для работы через Postman)
    data = request.get_json()
    form = RegistrationForm(data=data)

    if form.validate():
        return jsonify({"message": "Регистрация прошла успешно!"}), 200
    else:
        # Возвращаем список ошибок, если валидация не прошла
        return jsonify({"errors": form.errors}), 400


if __name__ == '__main__':
    app.run(debug=True)
