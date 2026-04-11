import subprocess
import os
import signal
import shlex


def release_port_and_run(port: int):
    # 1. Ищем процесс, который занял порт.
    # Флаг -t в lsof выводит только PID (число), что нам и нужно.
    command = f"lsof -i :{port} -t"

    try:
        # Выполняем команду и получаем список PID
        output = subprocess.check_output(shlex.split(command)).decode().strip()

        if output:
            # lsof может вернуть несколько PID через перенос строки
            pids = output.split('\n')
            for pid in pids:
                print(f"--- Порт {port} занят процессом {pid}. Завершаю его... ---")
                # 2. Завершаем процесс (SIGTERM — вежливое завершение)
                os.kill(int(pid), signal.SIGTERM)

    except subprocess.CalledProcessError:
        # Если lsof ничего не нашел, он вернет ошибку выполнения — это значит порт свободен
        print(f"--- Порт {port} свободен. ---")

    # 3. Теперь запускаем наш сервер (для примера выведем сообщение)
    print(f"--- Запускаю сервер на порту {port}... ---")
    # Здесь должен быть твой app.run(port=port)
# ... (весь предыдущий код функции выше) ...

if __name__ == '__main__':
    # Вызываем функцию для порта 5000 (или любого другого)
    release_port_and_run(5000)
