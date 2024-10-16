from flask import Blueprint, url_for, redirect, render_template, request, make_response, render_template_string
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним' # получаем куки из запроса request
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or 'неизвестно'
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/')) # создали ответ, ...
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp # ... который можем посылать


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
        
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/paid')
def paid():
    return render_template('lab3/paid.html')


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        return resp

    color = request.cookies.get('color')
    resp = make_response(render_template('/lab3/settings.html', color=color))
    return resp


@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    return resp

if __name__ == '__main__':
    lab3.run(debug=True)


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        fio = request.form.get('fio')
        polka = request.form.get('polka')
        belie = request.form.get('belie')
        bagazh = request.form.get('bagazh')
        age = int(request.form.get('age'))
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date = request.form.get('date')
        insurance = request.form.get('insurance')

        # Логика расчета цены
        if age < 18:
            ticket_type = "Детский билет"
            price = 700
        else:
            ticket_type = "Взрослый билет"
            price = 1000

        if polka in ["нижняя", "нижняя боковая"]:
            price += 100
        if belie:
            price += 75
        if bagazh:
            price += 250
        if insurance:
            price += 150

        return render_template('lab3/ticket_result.html', fio=fio, polka=polka, ticket_type=ticket_type,
                               price=price, departure=departure, destination=destination, date=date)

    return render_template('lab3/ticket_form.html')


books = [
    {"title": "1984", "price": 379, "author": "Джордж Оруэлл", "genre": "Антиутопия"},
    {"title": "Убить пересмешника", "price": 125, "author": "Харпер Ли", "genre": "Классика"},
    {"title": "Великий Гэтсби", "price": 300, "author": "Фрэнсис Скотт Фицджеральд", "genre": "Классика"},
    {"title": "Гордость и предубеждение", "price": 185, "author": "Джейн Остин", "genre": "Роман"},
    {"title": "Над пропастью во ржи", "price": 253, "author": "Джером Дэвид Сэлинджер", "genre": "Подростковый роман"},
    {"title": "Моби Дик", "price": 500, "author": "Герман Мелвилл", "genre": "Приключения"},
    {"title": "Война и мир", "price": 850, "author": "Лев Толстой", "genre": "Исторический роман"},
    {"title": "Одиссея", "price": 250, "author": "Гомер", "genre": "Эпическая поэзия"},
    {"title": "О дивный новый мир", "price": 198, "author": "Олдос Хаксли", "genre": "Антиутопия"},
    {"title": "Преступление и наказание", "price": 490, "author": "Фёдор Достоевский", "genre": "Психологический роман"},
    {"title": "Властелин колец", "price": 630, "author": "Джон Рональд Руэл Толкин", "genre": "Фэнтези"},
    {"title": "Гарри Поттер и философский камень", "price": 512, "author": "Джоан Роулинг", "genre": "Фэнтези"},
    {"title": "Хоббит", "price": 470, "author": "Джон Рональд Руэл Толкин", "genre": "Фэнтези"},
    {"title": "Алхимик", "price": 240, "author": "Пауло Коэльо", "genre": "Фикшн"},
    {"title": "Маленький принц", "price": 158, "author": "Антуан де Сент-Экзюпери", "genre": "Детская литература"},
    {"title": "Код да Винчи", "price": 1105, "author": "Дэн Браун", "genre": "Мистика"},
    {"title": "Унесенные ветром", "price": 302, "author": "Маргарет Митчелл", "genre": "Исторический роман"},
    {"title": "Сияние", "price": 270, "author": "Стивен Кинг", "genre": "Ужасы"},
    {"title": "Голодные игры", "price": 360, "author": "Сьюзен Коллинз", "genre": "Антиутопия"},
    {"title": "Дорога", "price": 200, "author": "Кормак Маккарти", "genre": "Постапокалипсис"}
]

@lab3.route('/lab3/books')
def books_list():
    return render_template('lab3/books.html', books=books)

@lab3.route('/lab3/filter_books', methods=['GET', 'POST'])
def filter_books():
    if request.method == 'POST':
        min_price = float(request.form['min_price'])
        max_price = float(request.form['max_price'])
        filtered_books = [book for book in books if min_price <= book['price'] <= max_price]
        return render_template('lab3/filtered_books.html', books=filtered_books)
    return render_template('lab3/filter_form.html')

if __name__ == '__main__':
    lab3.run(debug=True)