from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                                                    # Создание  Flask-приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location_database.db' #  Конфигурация базы данных SQLite

# Инициализация SQLAlchemy с приложением Flask
db = SQLAlchemy(app)

# Определение модели данных для таблицы
class Colleagues_Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #   идентификатор
    name = db.Column(db.String(50))                 # Имя коллеги
    location = db.Column(db.String(50))             # Местоположение

    # Конструктор создания новых записей
    def __init__(self, name, location):
        self.name = name
        self.location = location

# Создание  таблиц в базе данных, если они еще не существуют
with app.app_context():
    db.create_all()

# Определение маршрута для добавления нового коллеги и его местоположения
@app.route('/add_colleague_and_location', methods=['POST'])
def add_colleague_and_location():
    name = request.form['name']                                  # Получение данных из POST-запроса
    location = request.form['location']

    colleague_and_location = Colleagues_Location(name, location) # Создание объекта Colleagues_Location
    db.session.add(colleague_and_location)                       # Добавление объекта и сохранение изменений в базе данных
    db.session.commit()
    return {"session": "colleagues_and_location added successfully"}

# Определение маршрута для получения информации о коллеге и его местоположении по id
@app.route('/get_colleague_and_location/<int:id>')
def get_colleague_and_location(id):
    colleague_and_location =Colleagues_Location.query.get(id)   # Поиск записи по id
    if colleague_and_location:                                  # Если запись найдена, возвращаем её данные в формате JSON
        return jsonify({
            'id': colleague_and_location.id,
            'name': colleague_and_location.name,
            'location': colleague_and_location.location
            })
    else:                                                       # Если запись не найдена, возвращаем сообщение об ошибке
        return {'error': 'colleague_and_location not found'}

# Запуск приложения на локальном сервере
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



