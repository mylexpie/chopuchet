from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Настройка базы данных через переменную окружения
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/dbname'
db = SQLAlchemy(app)

# Модель сотрудника
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)

# Модель смены
class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

# Создание таблиц
with app.app_context():
    db.create_all()

# API: Получить список сотрудников
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'position': e.position} for e in employees])

# API: Назначить смену
@app.route('/shifts', methods=['POST'])
def create_shift():
    data = request.json
    shift = Shift(
        employee_id=data['employee_id'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time'])
    )
    db.session.add(shift)
    db.session.commit()
    return jsonify({'message': 'Shift created'}), 201

if __name__ == '__main__':
    app.run(debug=True)