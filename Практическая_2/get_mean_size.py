import sys


def get_mean_size(lines):
    """
    Вычисляет средний размер файла на основе строк из ls -l.
    Размер файла находится в 5-й колонке (индекс 4).
    """
    total_size = 0
    file_count = 0

    for line in lines:
        columns = line.split()
        # Проверяем, что строка содержит данные о файле (обычно 9 колонок в ls -l)
        if len(columns) >= 5:
            try:
                # 5-й столбец — это размер в байтах
                file_size = int(columns[4])
                total_size += file_size
                file_count += 1
            except ValueError:
                # Пропускаем строки, где в 5-й колонке не число (например, заголовок)
                continue

    if file_count == 0:
        return 0

    return total_size / file_count


if __name__ == '__main__':
    # Читаем все строки из стандартного ввода, пропуская первую (total ...)
    input_data = sys.stdin.readlines()

    if not input_data:
        print("Ошибка: Входные данные пусты.")
    else:
        # Отбрасываем первую строку заголовка 'total'
        data_lines = input_data[1:]
        mean_size = get_mean_size(data_lines)

        if mean_size == 0:
            print("Файлы не найдены или их размер не удалось определить.")
        else:
            print(f"Средний размер файлов: {mean_size:.2f} байт")
