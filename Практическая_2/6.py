import os
from flask import Flask

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size, relative_path):
    # Определяем базовую директорию проекта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем абсолютный путь к запрашиваемому файлу
    abs_path = os.path.abspath(os.path.join(base_dir, relative_path))

    try:
        # Проверяем, существует ли файл
        if not os.path.exists(abs_path):
            return f"Файл по адресу {abs_path} не найден", 404

        with open(abs_path, 'r', encoding='utf-8') as file:
            # Читаем только необходимое количество символов (оптимизация по памяти)
            result_text = file.read(size)
            result_size = len(result_text)

        # Формируем HTML-ответ согласно условию
        # <b> - жирный текст, <br> - перенос строки
        return (
            f"<b>{abs_path}</b> {result_size}<br>"
            f"{result_text}"
        )

    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
