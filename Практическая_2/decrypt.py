import sys


def decrypt(cipher_text):
    """
    Расшифровывает строку по правилам:
    '.'  -> ничего не делает (просто удаляется)
    '..' -> удаляет предыдущий символ
    """
    result = []
    i = 0
    n = len(cipher_text)

    while i < n:
        # Проверяем, является ли текущий символ и следующий точками (две точки)
        if cipher_text[i] == '.' and i + 1 < n and cipher_text[i + 1] == '.':
            if result:
                result.pop()  # Стираем предыдущий символ
            i += 2  # Пропускаем обе точки
        # Проверяем на одну точку
        elif cipher_text[i] == '.':
            i += 1  # Просто пропускаем точку
        # Если это буква, пробел или другой символ
        else:
            result.append(cipher_text[i])
            i += 1

    return "".join(result)


if __name__ == '__main__':
    # Читаем данные из стандартного ввода (поддержка pipe)
    # Используем strip(), чтобы убрать лишний перенос строки от команды echo
    input_data = sys.stdin.read().strip()

    if input_data:
        decoded_message = decrypt(input_data)
        print(decoded_message)
    else:
        # Если вход пустой, выводим пустую строку
        print("")
