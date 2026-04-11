import os

# Путь к файлу вынесен в отдельную переменную
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, 'output_file.txt')


def format_bytes(size):
    """Преобразует число байт в человекочитаемый формат."""
    power = 1024
    n = 0
    power_labels = {0: 'B', 1: 'KiB', 2: 'MiB', 3: 'GiB', 4: 'TiB'}
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}"


def get_summary_rss(file_path):
    """Суммирует RSS из файла и возвращает строку с результатом."""
    total_rss = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        # Пропускаем заголовок (первую строку) с помощью среза
        lines = file.readlines()[1:]

        for line in lines:
            columns = line.split()
            if len(columns) >= 6:
                # RSS — это 6-й столбец (индекс 5). В ps aux он в килобайтах.
                # Переводим сразу в байты для универсальности format_bytes
                total_rss += int(columns[5]) * 1024

    return format_bytes(total_rss)


if __name__ == '__main__':
    # Перед запуском убедитесь, что файл создан командой: ps aux > output_file.txt
    if os.path.exists(OUTPUT_FILE):
        summary = get_summary_rss(OUTPUT_FILE)
        print(f"Суммарное потребление памяти (RSS): {summary}")
    else:
        print(f"Файл {OUTPUT_FILE} не найден. Сначала запустите 'ps aux > output_file.txt'")
