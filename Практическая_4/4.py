import subprocess
import shlex
from flask import Flask, request

# 1. Создаем объект приложения
app = Flask(__name__)


@app.route('/uptime', methods=['GET'])
def get_uptime():
    try:
        # Для macOS используем обычный uptime и немного магии строк
        result = subprocess.check_output(['uptime']).decode('utf-8').strip()

        # Находим часть после "up" и до запятой (время работы)
        if 'up' in result:
            uptime_part = result.split('up')[1].split(',')[0:2]
            uptime_value = ','.join(uptime_part).strip()
            return f"Current uptime is {uptime_value}"

        return f"Current uptime is {result}"
    except Exception as e:
        return f"Could not get uptime: {str(e)}", 500


@app.route('/ps', methods=['GET'])
def get_processes():
    # 2. Получаем список аргументов: /ps?arg=a&arg=u&arg=x
    args: list[str] = request.args.getlist('arg')

    # Экранируем каждый аргумент для безопасности
    clean_args = [shlex.quote(arg) for arg in args]

    # Собираем команду: ['ps', 'a', 'u', 'x']
    command = ['ps'] + clean_args

    try:
        # Выполняем и захватываем вывод (stdout)
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Оборачиваем в <pre>, чтобы в браузере была красивая таблица
        return f"<pre>{result.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Ошибка выполнения (возможно, неверный флаг): <pre>{e.stderr}</pre>", 400
    except Exception as e:
        return f"Произошла ошибка: {str(e)}", 500


if __name__ == '__main__':
    # Запускаем сервер на порту 5001
    app.run(debug=True, port=5001)
