from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/oak")
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


@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author") # redirect - перенаправление

@lab1.route("/lab1/created")
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


@lab1.route("/lab1")
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
@lab1.route('/400')
def bad_request():
    return "<h1>Ошибка 400: Неверный запрос</h1>", 400


@lab1.route('/401')
def unauthorized():
    return "<h1>Ошибка 401: Неавторизованный запрос</h1>", 401


@lab1.route('/402')
def payment_required():
    return "<h1>Ошибка 402: Требуется оплата</h1>", 402


@lab1.route('/403')
def forbidden():
    return "<h1>Ошибка 403: Доступ запрещен</h1>", 403


@lab1.route('/405')
def method_not_allowed():
    return "<h1>Ошибка 405: Метод не поддерживается</h1>", 405


@lab1.route('/418')
def im_a_teapot():
    return "<h1>Ошибка 418: Я чайник</h1>", 418


@lab1.route('/error')
def error():
    a = 1 / 0 # Деление на ноль
    
    
@lab1.errorhandler(500)
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


@lab1.route('/mef')
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

@lab1.route('/lab1/resource')
def resource():
    status = 'Ресурс ещё не создан'
    create_link = url_for('created')
    delete_link = url_for('delete')

    if create:
        status = 'Ресурс создан'
        delete_link = url_for('delete')

    return render_template('resource.html', status=status, create_link=create_link, delete_link=delete_link)
    

@lab1.route('/lab1/create')
def create():
    global create

    if not create:
        create = True
        return 'Успешно: ресурс создан', 201
    else:
        return 'Отказано: ресурс уже создан', 400

@lab1.route('/lab1/delete')
def delete():
    global create

    if create:
        create = False
        return 'Успешно: ресурс удалён', 200
    else:
        return 'Отказано: ресурс отсутствует', 400