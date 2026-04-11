from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Кортеж — самый оптимальный по памяти выбор для фиксированного набора данных
WEEKDAYS = (
    "понедельника",
    "вторника",
    "среды",
    "четверга",
    "пятницы",
    "субботы",
    "воскресенья"
)


@app.route('/hello-world/<name>')
def hello_world(name):
    # Получаем индекс текущего дня недели (0 - понедельник, 6 - воскресенье)
    weekday_index = datetime.today().weekday()
    day_name = WEEKDAYS[weekday_index]

    # Определяем правильное пожелание в зависимости от рода дня недели
    # Среда (2), Пятница (4), Суббота (5) — женский род ("Хорошей")
    if weekday_index in (2, 4, 5):
        wish = "Хорошей"
    else:
        wish = "Хорошего"

    return f"Привет, {name}. {wish} {day_name}!"


if __name__ == '__main__':
    app.run(debug=True)
