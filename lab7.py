from flask import Blueprint, render_template, request, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

films = [
    {
        "title": "It",
        "title_ru": "Оно",
        "year": 2017,
        "description": "Когда в городке Дерри штата Мэн начинают пропадать дети, несколько ребят сталкиваются со своими величайшими страхами — не только с группой школьных хулиганов, но со злобным клоуном Пеннивайзом, список жертв которого уходит вглубь веков."
    },

    {
        "title": "The Substance",
        "title_ru": "Субстанция",
        "year": 2024,
        "description": "Слава голливудской звезды Элизабет Спаркл осталась в прошлом, хотя она всё ещё ведёт фитнес-шоу на телевидении. Когда её передачу собираются перезапустить с ведущей помоложе, от отчаяния Элизабет решает принять инновационный препарат, создатели которого обещают невероятное преображение, но при соблюдении правила одной недели. Так на свет появляется молодая красотка Сью. Девушка начинает делать карьеру в шоу-бизнесе и вскоре решает, что семи дней ей маловато."
    },

    {
        "title": "Trance",
        "title_ru": "Транс",
        "year": 2013,
        "description": "Сотрудник аукционного дома Саймон отвечает за сохранность картин во время проведения аукциона и в случае опасности должен запереть картину в сейфе. Во время ограбления он получает удар по голове и просыпается в больнице с амнезией. Саймон единственный кто знает, где находится картина, которой нет ни в сейфе, ни у грабителей. Бандиты похищают и пытают его. А после неудавшейся попытки вспомнить, банда нанимает гипно-терапевта Элизабет, которая должна помочь Саймону восстановить воспоминания о местонахождении картины."
    },

    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кобб – талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий разум наиболее уязвим. Редкие способности Кобба сделали его ценным игроком в привычном к предательству мире промышленного шпионажа, но они же превратили его в извечного беглеца и лишили всего, что он когда-либо любил. "
    },

    {
        "title": "In Time",
        "title_ru": "Время",
        "year": 2011,
        "description": "Добро пожаловать в мир, где время стало единственной и самой твердой валютой, где люди генетически запрограммированы так, что в 25 лет перестают стареть. Правда, последующие годы стоят денег. И вот богатые становятся практически бессмертными, а бедные обречены сражаться за жизнь. Уилл, бунтарь из гетто, несправедливо обвинен в убийстве с целью грабежа времени и теперь вынужден, захватив заложницу, пуститься в бега."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film is None:
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    film = request.get_json()

    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({"error": "Русское название не может быть пустым"}), 400

    # Проверка оригинального названия
    if not film.get('title') and not film.get('title_ru'):
        return jsonify({"error": "Не указано ни оригинальное, ни русское название"}), 400

    # Проверка года
    try:
        year = int(film.get('year'))
        if year < 1895 or year > datetime.now().year:
            return jsonify({"error": f"Год должен быть от 1895 до {datetime.now().year}"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Год должен быть числом"}), 400

    # Проверка описания
    description = film.get('description')
    if not description:
        return jsonify({"error": "Описание не может быть пустым"}), 400
    if len(description) > 2000:
        return jsonify({"error": "Описание не должно превышать 2000 символов"}), 400

    # Если оригинальное название пустое, используем русское название
    if not film.get('title'):
        film['title'] = film['title_ru']

    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s 
        WHERE id = %s;
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    db_close(conn, cur)
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({"error": "Русское название не может быть пустым"}), 400

    # Проверка оригинального названия
    if not film.get('title') and not film.get('title_ru'):
        return jsonify({" error": "Не указано ни оригинальное, ни русское название"}), 400

    # Проверка года
    try:
        year = int(film.get('year'))
        if year < 1895 or year > datetime.now().year:
            return jsonify({"error": f"Год должен быть от 1895 до {datetime.now().year}"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Год должен быть числом"}), 400

    # Проверка описания
    description = film.get('description')
    if not description:
        return jsonify({"error": "Описание не может быть пустым"}), 400
    if len(description) > 2000:
        return jsonify({"error": "Описание не должно превышать 2000 символов"}), 400

    # Если оригинальное название пустое, используем русское название
    if not film.get('title'):
        film['title'] = film['title_ru']

    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (film['title'], film['title_ru'], film['year'], film['description']))
    new_id = cur.fetchone()
    db_close(conn, cur)
    return jsonify({"index": new_id}), 201