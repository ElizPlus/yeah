from flask import Blueprint, render_template, request, session, current_app, jsonify, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('/lab8/lab8.html', login=session.get('login'))

@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Введите имя пользователя')

    if not password_form:
        return render_template('lab8/register.html', error='Введит пароль')
    

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
       return render_template('lab8/register.html', error='Такой пользователь уже существует')
    

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический логин после регистрации
    login_user(new_user, remember=False)

    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')  # Получаем значение галочки

    if not login_form:
        return render_template('lab8/login.html', error='Введите имя пользователя')

    if not password_form:
        return render_template('lab8/login.html', error='Введит пароль')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me == 'on')  # Используем галочку 
            return redirect('/lab8/')
        
    
    return render_template('/lab8/login.html', error = "Ошибка взода: логин и/или пароль неверны")


@lab8.route('/lab8/articles')
@login_required     # страница доступна только авторизованным пользователям
def article_list():
    return "список статей"


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()   # функция удаления сессии
    return redirect('/lab8/')


@lab8.route('/lab8/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('/lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title:
        return render_template('lab8/create_article.html', error='Введите заголовок статьи')

    if not article_text:
        return render_template('lab8/create_article.html', error='Введите текст статьи')

    new_article = articles(
        login_id=current_user.id,  # ID текущего пользователя
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=True,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)

    if not article:
        return render_template('lab8/articles.html', error='Статья не найдена')

    if article.login_id != current_user.id:
        return render_template('lab8/articles.html', error='Вы не можете редактировать эту статью')

    if request.method == 'GET':
        return render_template('/lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title:
        return render_template('lab8/edit_article.html', error='Введите заголовок статьи')

    if not article_text:
        return render_template('lab8/edit_article.html', error='Введите текст статьи')

    article.title = title
    article.article_text = article_text
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)

    if not article:
        return render_template('lab8/articles.html', error='Статья не найдена')

    if article.login_id != current_user.id:
        return render_template('lab8/articles.html', error='Вы не можете удалить эту статью')

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/public_articles')
def public_articles():
    articles = articles.query.filter_by(is_public=True).all()  # Получаем только публичные статьи
    return render_template('lab8/public_articles.html', articles=articles)


@lab8.route('/lab8/search_articles', methods=['GET', 'POST'])
@login_required
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search_articles.html')
    
    search_query = request.form.get('search_query')

    if not search_query:
        return render_template('lab8/search_articles.html', error='Введите строку для поиска')

    # Поиск по публичным статьям и статьям текущего пользователя
    user_articles = articles.query.filter(
        (articles.login_id == current_user.id) | (articles.is_public == True)
    ).filter(
        (articles.title.contains(search_query)) | (articles.article_text.contains(search_query))
    ).all()

    return render_template('lab8/search_results.html', articles=user_articles, search_query=search_query)