from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from db import db
import os
from os import path

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'ivan_ivanov_orm'
    db_user = 'ivan_ivanov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.errorhandler(404)
def not_found(err):
    image = url_for("static", filename="page.gif")
    return '''
    <!doctype html> 
    <html>
    <head>
        <style>
            img {
                width: 100%;          
                height: auto;          
                display: block;       
            }
            </style> 
    </head>
        <body> 
            <img src="''' + image + '''"> 
            <p style="text-align: right;"><i>Кнопка "Go to homepage" фальшивая:)</i></p>
        </body> 
    </html>
    ''', 404


@app.route("/")
@app.route("/index")
def nstu():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <li><a href="/lab1">Первая лабораторная</a></li>
        <li><a href="/lab2/">Вторая лабораторная</a></li>
        <li><a href="/lab3/">Третья лабораторная</a></li>
        <li><a href="/lab4/">Четвёртая лабораторная</a></li>
        <li><a href="/lab5/">Пятая лабораторная</a></li>
        <li><a href="/lab6/">Шестая лабораторная</a></li>
        <li><a href="/lab7/">Седьмая лабораторная</a></li>
        <li><a href="/lab8/">Восьмая лабораторная</a></li>
    <footer>
        <p>&copy; Плюснина Елизавета Евгеньевна, ФБИ-22, 3 курс, 2024</p>
    </footer>
    </body> 
</html>
'''

# Коды ответа HTTP
@app.route('/400')
def bad_request():
    return "<h1>Ошибка 400: Неверный запрос</h1>", 400


@app.route('/401')
def unauthorized():
    return "<h1>Ошибка 401: Неавторизованный запрос</h1>", 401


@app.route('/402')
def payment_required():
    return "<h1>Ошибка 402: Требуется оплата</h1>", 402


@app.route('/403')
def forbidden():
    return "<h1>Ошибка 403: Доступ запрещен</h1>", 403


@app.route('/405')
def method_not_allowed():
    return "<h1>Ошибка 405: Метод не поддерживается</h1>", 405


@app.route('/418')
def im_a_teapot():
    return "<h1>Ошибка 418: Я чайник</h1>", 418


@app.route('/error')
def error():
    a = 1 / 0 # Деление на ноль
    
    
@app.errorhandler(500)
def internal_server_error(error):
    return '''
<!doctype html> 
<html>
    <body> 
        <h1>Ошибка на сервере 505</h1>
        <p>Ну да, ага</p>
    </body> 
</html>
''', 500

