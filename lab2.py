from flask import Blueprint, url_for, redirect, render_template, request, abort
lab2 = Blueprint('lab2', __name__)



@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['орхидея', 'гибискус', 'гипсофила', 'фиалка']
flower_prices = {'орхидея': 100, 'гибискус': 50, 'гипсофила': 30, 'фиалка': 20}

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        flower_name = flower_list[flower_id]
        flower_price = flower_prices.get(flower_name)
        return render_template('flower.html', flower_name=flower_name, flower_price=flower_price)


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        flower_list.pop(flower_id)
        return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/add_flower/', defaults={'name': None})
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    if name is None:
        return "Вы не задали имя цветка", 400
    else:
        flower_list.append(name)
        return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/all_flowers')
def all_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Список всех цветов</h1>
        <ul>
            <p>Всего цветов: {len(flower_list)} </p>
            <p>Полный список:</p>
            <ul>
                {''.join([f'<li>{flower} <a href="/lab2/delete_flower/{i}">удалить</a></li>' for i, flower in enumerate(flower_list)])}
            </ul>
        </ul>
        <form action="/lab2/add_flower" method="get">
            <input type="text" name="name" placeholder="Название нового цветка">
            <button type="submit">Добавить цветок</button>
        </form>
        <a href="/lab2/delete_all_flowers">Удалить все цветы</a>
        </body>
    </html>
    '''

@lab2.route('/lab2/delete_all_flowers')
def delete_all_flowers():
    global flower_list
    flower_list = []
    return redirect(url_for('lab2.all_flowers'))


@lab2.route('/lab2/clear')
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


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@lab2.route('/lab2/calc/')
def calc_redirect():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/1/1')
def calc2():
    a = 1
    b = 1
    return render_template('calc.html', a=a, b=b)

@lab2.route('/lab2/calc/<int:a>')
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

@lab2.route('/lab2/books')
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

@lab2.route('/lab2/cats')
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
    
