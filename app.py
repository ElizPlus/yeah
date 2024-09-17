from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
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