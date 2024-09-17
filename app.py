from flask import Flask, url_for, redirect
app = Flask(__name__)

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



@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html> 
           <body> 
               <h1>web-сервер на flask</h1>
               <a href="/ab1/author">author</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": 'text/plain; charset=utf-8'
            }


@app.route("/lab1/author")
def author():
    name = "Плюснина Елизавета Евгеньевна" 
    group = "ФБИ-22"
    faculty = "ФБ"
    
    return """<!doctype html> 
        <html>
           <body> 
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
           </body> 
        </html>"""



@app.route("/lab1/oak")
def oak(): 
    img = url_for("static", filename="oak.jpg")  
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html> 
<html>
    <body> 
        <h1>Дуб</h1>
        <img src="''' + img + '''">
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''"> 
    </body> 
</html>
'''
count = 0


@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html> 
<html>
    <body> 
        Сколько раз вы заходили сюда: ''' + str(count) + '''
        <br>
        <a href="/lab1/reset_counter">Обнулить счётчик</a>
    </body> 
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html> 
<html>
    <body> 
        Счётчик обнулен. 
        <br>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body> 
</html>
'''


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author") # redirect - перенаправление

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i><div>
    </body>
</html>
''', 201


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

    <footer>
        <p>&copy; Плюснина Елизавета Евгеньевна, ФБИ-22, 3 курс, 2024</p>
    </footer>
    </body> 
</html>
'''

@app.route("/lab1")
def nstu2():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <div>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности
        </div>
        <li><a href="/">Ссылка на корень сайта</a></li>
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
    return "Результат: " + a # Конкатенация числа и строки

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