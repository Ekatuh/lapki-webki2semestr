from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, jsonify
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db import db
from db.models import User, Article
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime


lab8 = Blueprint('lab8', __name__, static_folder='static')

@lab8.route('/lab8/')
def lab():
    username = session.get('login', '')
    return render_template('lab8/lab8.html', login=session.get('login'), username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')

        if not login_form:
            error = 'Имя пользователя не должно быть пустым'
        elif not password_form:
            error = 'Пароль не должен быть пустым'
        else:
            login_exists = User.query.filter_by(login=login_form).first()
            if login_exists:
                error = 'Такой пользователь уже существует'
            else:
                password_hash = generate_password_hash(password_form)
                new_user = User(login=login_form, password=password_hash)
                db.session.add(new_user)
                db.session.commit()
                
                login_user(new_user) 
                session['login'] = new_user.login 
                return redirect('/lab8/')  

    return render_template('lab8/register.html', error=error)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        remember = request.form.get('remember')  # Получаем значение чекбокса

        if not login_form:
            error = 'Имя пользователя не должно быть пустым'
        elif not password_form:
            error = 'Пароль не должен быть пустым'
        else:
            user = User.query.filter_by(login=login_form).first()
            if user and check_password_hash(user.password, password_form):
                login_user(user, remember=remember)  # Используем remember
                session['login'] = user.login  # Сохраняем логин в сессии
                return redirect('/lab8/')
            else:
                error = 'Ошибка входа: логин и/или пароль неверны'

    return render_template('lab8/login.html', error=error)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None) 
    return redirect('/lab8/')  

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('content')
        is_public = request.form.get('is_public') == 'on'  # Получаем значение чекбокса

        new_article = Article(title=title, article_text=article_text, login_id=current_user.id, is_public=is_public)
        
        db.session.add(new_article)
        db.session.commit()
        return redirect('/lab8/')
    
    return render_template('lab8/create_article.html')

@lab8.route('/lab8/articles/')
def article_list():
    search_query = request.args.get('search')  # Получаем строку поиска из параметров запроса

    if current_user.is_authenticated:
        # Если пользователь авторизован, показываем все публичные статьи и непубличные статьи, созданные им
        if search_query:
            articles = Article.query.filter(
                (Article.is_public == True) | (Article.login_id == current_user.id),
                (Article.title.ilike(f'%{search_query}%') | Article.article_text.ilike(f'%{search_query}%'))
            ).all()
        else:
            articles = Article.query.filter(
                (Article.is_public == True) | (Article.login_id == current_user.id)
            ).all()
    else:
        # Если пользователь не авторизован, показываем только публичные статьи
        if search_query:
            articles = Article.query.filter(
                Article.is_public == True,
                (Article.title.ilike(f'%{search_query}%') | Article.article_text.ilike(f'%{search_query}%'))
            ).all()
        else:
            articles = Article.query.filter_by(is_public=True).all()

    for article in articles:
        article.user_login = User.query.get(article.login_id).login  # Получаем логин пользователя
    return render_template('lab8/article_list.html', articles=articles)


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)  # Получаем статью по ID

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('content')  # Получаем новое содержимое статьи

        # Обновляем данные статьи
        article.title = title
        article.article_text = article_text
        db.session.commit()  # Сохраняем изменения в базе данных
        return redirect('/lab8/articles/')  # Перенаправляем на страницу списка статей

    return render_template('lab8/edit_article.html', article=article)

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)  # Получаем статью по ID
    db.session.delete(article)  # Удаляем статью из сессии
    db.session.commit()  # Сохраняем изменения в базе данных
    return redirect('/lab8/articles/') 