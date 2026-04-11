# Глобальный список машин
CARS_LIST = ["Chevrolet", "Renault", "Ford", "Lada"]

@app.route('/cars')
def cars():
    # Метод join объединяет элементы списка в одну строку через запятую
    return ", ".join(CARS_LIST)

if __name__ == '__main__':
    app.run(debug=True)