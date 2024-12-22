from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, jsonify
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db import db
from db.models import User, Article
from datetime import datetime


lab8 = Blueprint('lab8', __name__, static_folder='static')

@lab8.route('/lab8/')
def lab():
  username = session.get('login', '')
  return render_template('lab8/lab8.html', login=session.get('login'), username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустое имя пользователя
    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')

    # Проверка на пустой пароль
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = User.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = User(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')
