from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, NumberRange, Optional

# 1. СНАЧАЛА создаем объект приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# 2. Описываем класс формы
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    index = IntegerField('Index', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional()])

# 3. ПОТОМ описываем маршрут (теперь 'app' определен)
@app.route('/registration', methods=['POST'])
def registration():
    # Если данные приходят из Postman в формате JSON
    form = RegistrationForm(data=request.get_json())

    if form.validate():
        return "Регистрация прошла успешно!", 200
    else:
        return jsonify(errors=form.errors), 400

if __name__ == '__main__':
    app.run(debug=True)
