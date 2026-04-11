from flask import Flask

app = Flask(__name__)

# Хранилище данных: { год: { месяц: сумма_трат } }
# Использование словаря позволяет получать данные за O(1)
storage = {}


@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    # Извлекаем год и месяц из строки YYYYMMDD
    year = int(date[:4])
    month = int(date[4:6])

    # Инициализируем вложенные словари, если их еще нет, и прибавляем трату
    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number

    return f"Запись сохранена: {number} руб. за {date}"


@app.route('/calculate/<int:year>')
def calculate_year(year):
    # Проверяем наличие данных за год
    if year not in storage:
        return f"Данные за {year} год отсутствуют.", 404

    # Суммируем все значения (траты по месяцам) внутри года
    total_year = sum(storage[year].values())
    return f"Суммарные траты за {year} год: {total_year} руб."


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    # Проверяем наличие данных за конкретный месяц
    if year in storage and month in storage[year]:
        total_month = storage[year][month]
        return f"Суммарные траты за {month:02d}.{year}: {total_month} руб."

    return f"Данные за {month:02d}.{year} не найдены.", 404


if __name__ == '__main__':
    # Используйте 127.0.0.1 вместо 127.0.0.5
    app.run(host='127.0.0.1', port=5000, debug=True)