from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers_path>')
def max_number(numbers_path):
    # Разделяем путь по слэшам и убираем пустые элементы (если в конце был /)
    parts = [p for p in numbers_path.split('/') if p]

    try:
        # Преобразуем строки в числа (float для поддержки дробных чисел)
        nums = [float(p) for p in parts]

        if not nums:
            return "Ошибка: не передано ни одного числа."

        # Находим максимальное число
        max_num = max(nums)

        # Если число целое (например, 10.0), убираем десятичную часть для красоты
        if max_num.is_integer():
            max_num = int(max_num)

        return f"Максимальное число: <i>{max_num}</i>"

    except ValueError:
        # Если в URL попало что-то, что нельзя превратить в число
        return "Ошибка: в пути должны быть только числа, разделённые слэшем."


if __name__ == '__main__':
    app.run(debug=True)
