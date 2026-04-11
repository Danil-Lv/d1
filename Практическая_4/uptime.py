import subprocess
from flask import Flask

# 1. Создаем объект приложения
app = Flask(__name__)


@app.route('/uptime', methods=['GET'])
def get_uptime():
    try:
        # Выполняем обычный uptime без флагов
        result = subprocess.check_output(['uptime']).decode('utf-8').strip()

        # На macOS результат выглядит так:
        # 11:35  up 2 days, 14:21, 3 users, load averages: 1.20 1.45 1.60
        # Нам нужно то, что между "up" и второй запятой

        if 'up' in result:
            # Отрезаем всё до слова "up" и берем часть до информации о пользователях
            uptime_info = result.split('up')[1].split(',')[0:2]
            uptime_value = ','.join(uptime_info).strip()
            return f"Current uptime is {uptime_value}"

        return f"Current uptime is {result}"
    except Exception as e:
        return f"Could not get uptime: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Используем другой порт, чтобы не конфликтовать
