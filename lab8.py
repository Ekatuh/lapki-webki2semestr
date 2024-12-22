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
                return redirect('/lab8/')

    return render_template('lab8/register.html', error=error)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')

        if not login_form:
            error = 'Имя пользователя не должно быть пустым'
        elif not password_form:
            error = 'Пароль не должен быть пустым'
        else:
            user = User.query.filter_by(login=login_form).first()
            if user and check_password_hash(user.password, password_form):
                login_user(user, remember=False)
                session['login'] = user.login  # Сохраняем логин в сессии
                return redirect('/lab8/')
            else:
                error = 'Ошибка входа: логин и/или пароль неверны'

    return render_template('lab8/login.html', error=error)

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect('/lab8/')  # Перенаправляем на главную страницу
