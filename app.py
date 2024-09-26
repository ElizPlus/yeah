from flask import Flask, url_for, redirect, render_template, request, abort
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
        <h2>Список роутов</h2>
        <li><a href="404">Ссылка на ошибку 404</a></li>
        <li><a href="/lab1/web">Ссылка на web-сервер на flask</a></li>
        <li><a href="/lab1/author">Ссылка на автора</a></li>
        <li><a href="/lab1/oak">Ссылка на дуб</a></li>
        <li><a href="/lab1/counter">Ссылка на счётчик</a></li>
        <li><a href="/lab1/reset_counter">Ссылка на обнуление счётчика</a></li>
        <li><a href="/lab1/info">Ссылка на перенаправление</a></li>
        <li><a href="/lab1/created">Ссылка на что-то</a></li>
        <li><a href="/index">Ссылка на корень сайта</a></li>
        <li><a href="/400">Ссылка на ошибку 400</a></li>
        <li><a href="/401">Ссылка на ошибку 401</a></li>
        <li><a href="/402">Ссылка на ошибку 402</a></li>
        <li><a href="/403">Ссылка на ошибку 403</a></li>
        <li><a href="/405">Ссылка на ошибку 405</a></li>
        <li><a href="/418">Ссылка на ошибку 418</a></li>
        <li><a href="/error">Ошибка на ошибку</a></li>
        <li><a href="/mef">Ссылка на мой текст</a></li>
        
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


@app.route('/mef')
def mb():
    img = url_for("static", filename="dep.jpg")
    headers = {
        'Content-Language': 'ru', # страница на русском языке
        'X-My-Header': 'Hello', 
        'X-Another-Header': 'World' # нестандартные заголовки, которые используются для передачи дополнительной информации
    }
    return '''
<!doctype html> 
<html>
    <body> 
        <h1>Глава 1 Рандеву с неудачником</h1>
        <p>Москва еще не успела остыть после жаркого и душного июньского дня. Солнце, запыхавшись, лежало на крышах и отдувалось, однако у самой земли уже бродили смутные вечерние тени. Водосточная труба, к которой Дафна походя прикоснулась ладонью, 
        была обжигающе горячей. Даф поморщилась. Стараясь ничем не выделяться среди обычных людей, она не так давно отрегулировала свой болевой порог, сделав его, как у лопухоидов, и теперь не уставала удивляться новым ощущениям, 
        постоянно делая какое-нибудь новое открытие.</p>
        <img src="''' + img + '''">
        <p>Например, выпив в задумчивости кипящей воды, можно согреться на всю оставшуюся жизнь. Новая обувь причиняет массу неудобств. Прикушенный кончик языка болит целую неделю. Если сразу после чая приняться за мороженое – зубы начинают ныть, 
        а эмаль трескается, как древние скалы. Романтично побегав по лужам босиком, легко поймать ступней зазубренное донышко бутылки. В общем, не жизнь у лопухоидов, а сплошные ограничения. Столько всякой ерунды приходится помнить!</p>
        <p>Лавируя между прохожими, Даф продолжала свою прогулку, не имевшую ни определенной цели, ни маршрута. В доме № 13 по Большой Дмитровке в этот час принимали отчеты суккубов и комиссионеров. Арей вежливо попросил 
        Даф куда-нибудь сгинуть и не распугивать нервный темный народец своей светлой сущностью и торчащей из рюкзака флейтой. Даф и сама рада была уйти. Пришибленные пластилиновые физиономии мало вдохновляли ее на продолжение 
        знакомства и вообще на созидательный труд.</p>
    </body> 
</html>
''', 200, headers




create = False

@app.route('/lab1/resource')
def resource():
    status = 'Ресурс ещё не создан'
    create_link = url_for('created')
    delete_link = url_for('delete')

    if create:
        status = 'Ресурс создан'
        delete_link = url_for('delete')

    return render_template('resource.html', status=status, create_link=create_link, delete_link=delete_link)
    

@app.route('/lab1/create')
def create():
    global create

    if not create:
        create = True
        return 'Успешно: ресурс создан', 201
    else:
        return 'Отказано: ресурс уже создан', 400

@app.route('/lab1/delete')
def delete():
    global create

    if create:
        create = False
        return 'Успешно: ресурс удалён', 200
    else:
        return 'Отказано: ресурс отсутствует', 400
    

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['орхидея', 'гибискус', 'гипсофила', 'фиалка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        return f'''
        <!doctype html>
        <html>
            <body>
                <p>Цветок: {flower_list[flower_id]}</p>
                <a href="/lab2/all_flowers">Ссылка на страницу вывода всех цветов</a>
            </body>
        </html>
        '''


@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)

    if name is None:
        return "Вы не задали имя цветка", 400
    else:
        return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name} </p>
        <p>Всего цветов: {len(flower_list)} </p>
        <p>Полный список: {flower_list} </p>
        </body>
    </html>
    '''

@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Список всех цветов</h1>
        <ul>
            <p>Всего цветов: {len(flower_list)} </p>
            <p>Полный список: {flower_list} </p>
        </ul>
        </body>
    </html>
    '''

@app.route('/lab2/clear')
def clear():
    flower_list.clear()
    return f'''
      <!doctype html>
    <html>
        <body>
            <p>Список цветов очищен</p>
            <p><a href="/lab2/all_flowers">Ссылка на страницу вывода всех цветов</a></p>
        </body>
    </html>
    ''' , 200


@app.route('/lab2/example')
def example():
    name = 'Елизавета Плюснина'
    number = 2
    group = 'ФБИ-22'
    course = 3
    fruits = [
        {'name': 'манго', 'price': 150}, 
        {'name': 'бананы', 'price': 70},
        {'name': 'помело', 'price': 200},
        {'name': 'абрикосы', 'price': 90},
        {'name': 'нектарины', 'price': 110},
        ]
    return render_template('example.html', name=name, number=number, group=group, course=course, fruits=fruits)


@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/')
def calc_redirect():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/1/1')
def calc2():
    a = 1
    b = 1
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {"author": "Дмитрий Емец", "title": "Мефодий Буслаев", "genre": "Фэнтези", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 158},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Донна Тартт", "title": "Щегол", "genre": "Роман", "pages": 832},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
    {"author": "Мариам Петросян", "title": "Дом, в котором…", "genre": "Роман", "pages": 448},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Раиса Белоглазова", "title": "Ритка", "genre": "Повесть", "pages": 416},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Джек Лондон", "title": "Белый Клык", "genre": "Повесть", "pages": 336}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)



cats_list = [
    {
        'name': 'Шотландская',
        'description': 'Шотландская вислоухая кошка — это порода домашних кошек с характерными загнутыми вперед ушами.'
    },
    {
        'name': 'Британская',
        'description': 'Британская короткошерстная кошка — это крепко сложенная, коренастая кошка с округлыми чертами лица.'
    },
    {
        'name': 'Бенгальская',
        'description': 'Бенгальская кошка — это порода домашних кошек, известная своим пятнистым окрасом и энергичным характером.'
    },
    {
        'name': 'Мейн-кун',
        'description': 'Мейн-кун — это крупная порода домашних кошек с длинной шерстью и характерным окрасом.'
    },
    {
        'name': 'Персидская',
        'description': 'Персидская кошка — это порода домашних кошек с длинной шерстью и плоской мордой.'
    }
]

@app.route('/lab2/cats')
def show_cats():
    img_files = ["schot.png", "brit.jpeg", "bengal.jpg", "kun.jpg", "pers.jpg"]
    html = '''
    <!doctype html>
    <html>
        <body>
            <ul>
    '''
    for i, cat in enumerate(cats_list):
        img_url = url_for("static", filename=img_files[i])
        html += f'''
                <li>
                    <h2>{cat['name']}</h2>
                    <img src="{img_url}" width="300">
                    <p>{cat['description']}</p>
                </li>
        '''
    html += '''
        </body>
    </html>
    '''
    return html
    
