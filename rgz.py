from flask import Blueprint, render_template, request, redirect, session, flash, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db.models import User, Session
from . import db
from datetime import datetime
import re
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    print(current_app.config['DB_TYPE'])
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'elizaveta_plyusnina_knowledge_base',
            user = 'elizaveta_plyusnina_knowledge_base',
            password = '0113'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Глобальные переменные для хранения данных
users = {
    'admin': {
        'password_hash': generate_password_hash('111'),
        'name': 'Администратор'
    }
}
sessions = [
    {'id': 1, 'movie': 'Начало', 'date': '2024-12-21', 'time': '18:00'},
    {'id': 2, 'movie': 'Время', 'date': '2024-12-29', 'time': '20:00'},
    {'id': 3, 'movie': 'Субстанция', 'date': '2024-12-31', 'time': '15:00'},
]
bookings = {}  # {session_id: {seat_number: username}}

# Валидация входных данных
def validate_username(username):
    if not username:
        return False
    pattern = r'^[a-zA-Z0-9._-]+$'
    return re.match(pattern, username) is not None

def validate_password(password):
    if not password:
        return False
    pattern = r'^[a-zA-Z0-9._-]+$'
    return re.match(pattern, password) is not None


@rgz.route('/rgz/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect('/rgz/sessions')
    return render_template('/rgz/index.html')



@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Валидация логина
        if not validate_username(login):
            flash('Логин должен состоять только из латинских букв, цифр и знаков препинания (._-)')
            return redirect('/rgz/register')

        # Валидация пароля
        if not validate_password(password):
            flash('Пароль должен состоять только из латинских букв, цифр и знаков препинания (._-)')
            return redirect('/rgz/register')

        # Проверка, существует ли пользователь
        user = User.query.filter_by(login=login).first()
        if user:
            flash('Логин уже занят')
            return redirect('/rgz/register')

        # Создание нового пользователя
        new_user = User(login=login, password=generate_password_hash(password), name=name)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно')
        return redirect('/rgz/login')

    return render_template('/rgz/register.html')


@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']

        # Валидация логина
        if not validate_username(login):
            flash('Логин должен состоять только из латинских букв, цифр и знаков препинания (._-)')
            return redirect('/rgz/login')

        # Валидация пароля
        if not validate_password(password):
            flash('Пароль должен состоять только из латинских букв, цифр и знаков препинания (._-)')
            return redirect('/rgz/login')

        # Проверка, существует ли пользователь
        user = User.query.filter_by(login=login).first()
        if not user or not check_password_hash(user.password, password):
            flash('Неверное имя пользователя или пароль')
            return redirect('/rgz/login')

        # Сохранение пользователя в сессии
        session['user_id'] = user.id
        flash('Вход выполнен успешно')
        return redirect('/rgz/sessions')

    return render_template('/rgz/login.html')


@rgz.route('/rgz/logout')
def logout():
    session.pop('username', None)
    flash('Выход выполнен успешно')
    return redirect('/rgz/')


@rgz.route('/rgz/sessions')
def sessions_list():
    if 'username' not in session:
        return redirect('/rgz/login')

    return render_template('/rgz/sessions.html', sessions=sessions)


@rgz.route('/rgz/session/<int:session_id>', methods=['GET', 'POST'])
def session_details(session_id):
    if 'username' not in session:
        return redirect('/rgz/login')

    session_data = next((s for s in sessions if s['id'] == session_id), None)
    if not session_data:
        flash('Сеанс не найден')
        return redirect('/rgz/sessions')

    current_time = datetime.now()
    session_datetime = datetime.strptime(f"{session_data['date']} {session_data['time']}", '%Y-%m-%d %H:%M')
    is_past = session_datetime < current_time

    if request.method == 'POST':
        seat_number = int(request.form['seat_number'])
        print(f"Попытка забронировать место {seat_number} пользователем {session['username']}")  # Отладочный вывод

        # Проверка, является ли сеанс прошедшим
        if is_past:
            flash('Нельзя бронировать места на прошедший сеанс')
            return redirect(f'/rgz/session/{session_id}')

        if seat_number < 1 or seat_number > 30:
            flash('Некорректный номер места')
            return redirect(f'/rgz/session/{session_id}')

        if session_id not in bookings:
            bookings[session_id] = {}

        # Проверка, занято ли место другим пользователем
        if seat_number in bookings[session_id] and bookings[session_id][seat_number] != session['username']:
            flash('Место уже занято')
            return redirect(f'/rgz/session/{session_id}')

        # Проверка, сколько мест уже забронировано текущим пользователем
        user_bookings = sum(1 for seat, user in bookings[session_id].items() if user == session['username'])
        if user_bookings >= 5 and seat_number not in bookings[session_id]:
            flash('Вы не можете забронировать более 5 мест')
            return redirect(f'/rgz/session/{session_id}')

        # Бронирование или отмена бронирования места
        if seat_number in bookings[session_id] and bookings[session_id][seat_number] == session['username']:
            del bookings[session_id][seat_number]
            flash('Бронирование места отменено')
        else:
            bookings[session_id][seat_number] = session['username']
            flash('Место успешно забронировано')

        return redirect(f'/rgz/session/{session_id}')

    return render_template(
        '/rgz/session_details.html',
        session=session_data,
        seats=bookings.get(session_id, {}),
        is_past=is_past,
        username=session.get('username')  # Передаём текущего пользователя
    )


@rgz.route('/rgz/admin/sessions', methods=['GET', 'POST'])
def admin_sessions():
    if 'user_id' not in session or session['user_id'] != 1:  # Проверка, является ли пользователь администратором
        flash('Доступ запрещён')
        return redirect('/rgz/')

    if request.method == 'POST':
        movie = request.form['movie']
        date = request.form['date']
        time = request.form['time']

        if not movie or not date or not time:
            flash('Все поля обязательны')
            return redirect('/rgz/admin/sessions')

        # Создание нового сеанса
        new_session = Session(movie=movie, date=date, time=time)
        db.session.add(new_session)
        db.session.commit()

        flash('Сеанс добавлен')
        return redirect('/rgz/admin/sessions')

    sessions = Session.query.all()
    return render_template('/rgz/admin_sessions.html', sessions=sessions)




@rgz.route('/rgz/admin/session/<int:session_id>/delete', methods=['POST'])
def delete_session(session_id):
    if 'username' not in session or session['username'] != 'admin':
        flash('Доступ запрещён')
        return redirect('/rgz/')

    session_to_delete = next((s for s in sessions if s['id'] == session_id), None)
    if session_to_delete:
        sessions.remove(session_to_delete)
        if session_id in bookings:
            del bookings[session_id]
        flash('Сеанс удалён')
    else:
        flash('Сеанс не найден')

    return redirect('/rgz/admin/sessions')


@rgz.route('/rgz/admin/session/<int:session_id>/unbook', methods=['POST'])
def unbook_seat(session_id):
    if 'username' not in session or session['username'] != 'admin':
        flash('Доступ запрещён')
        return redirect('/rgz/')

    seat_number = int(request.form['seat_number'])
    if session_id in bookings and seat_number in bookings[session_id]:
        del bookings[session_id][seat_number]
        flash('Бронь снята')
    else:
        flash('Место не занято')

    return redirect(f'/rgz/session/{session_id}')


@rgz.route('/rgz/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        flash('Доступ запрещён')
        return redirect('/rgz/')

    username = session['username']

    # Удаляем пользователя из словаря users
    if username in users:
        del users[username]

    # Удаляем бронирования пользователя
    for session_id, seats in bookings.items():
        bookings[session_id] = {seat: user for seat, user in seats.items() if user != username}

    # Удаляем пользователя из сессии
    session.pop('username', None)

    flash('Аккаунт успешно удалён')
    return redirect('/rgz/')