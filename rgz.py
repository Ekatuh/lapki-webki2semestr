from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from os import path
from werkzeug.utils import secure_filename
import re


rgz = Blueprint('rgz', __name__, static_folder='static')

def db_connect():

    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(dbname="RGZshka", 
        user="postgres", 
        password="katya9056", 
        host="127.0.0.1"
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)

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

@rgz.route('/rgz/')
def lab():
    username = session.get('login', '')
    return render_template('/rgz/index.html', login=username)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def is_valid_username_password(value):
    # Проверяем, что строка состоит только из латинских букв, цифр и знаков препинания
    return bool(re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=-]*$', value))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    username = request.form.get('username')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    search_gender = request.form.get('search_gender')
    about = request.form.get('about')
    photo = request.files.get('photo')

    # Валидация логина и пароля
    if not (username and password and full_name and age and gender and search_gender):
        return render_template('rgz/register.html', error='Заполните все обязательные поля')

    if not is_valid_username_password(username) or not is_valid_username_password(password):
        return render_template('rgz/register.html', error='Логин и пароль могут содержать только латинские буквы, цифры и знаки препинания.')

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)
    else:
        return render_template('rgz/register.html', error='Недопустимый формат изображения')

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT username FROM users WHERE username=%s;", (username,))
        else:
            cur.execute("SELECT username FROM users WHERE username=?;", (username,))

        if cur.fetchone():
            return render_template('rgz/register.html', error="Такой пользователь уже существует")

        password_hash = generate_password_hash(password)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO users (username, password_hash, full_name, age, gender, search_gender, about, photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (username, password_hash, full_name, age, gender, search_gender, about, photo_path))
        else:
            cur.execute("""
                INSERT INTO users (username, password_hash, full_name, age, gender, search_gender, about, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (username, password_hash, full_name, age, gender, search_gender, about, photo_path))

        conn.commit()
    finally:
        db_close(conn, cur)

    return render_template('rgz/success.html', username=username)

@rgz.route('/api/upload', methods=['POST']) 
def upload_image(): 
    if 'photo' not in request.files: 
        return {'error': 'No file part'}, 400
    photo = request.files['photo']
    if photo.filename == '':
        return {'error': 'No selected file'}, 400

    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)
        return {'message': 'File uploaded successfully', 'filename': filename}, 201
    else:
        return {'error': 'Invalid file format'}, 400

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # Валидация логина и пароля
    if not is_valid_username_password(username) or not is_valid_username_password(password):
        return render_template('rgz/login.html', error='Логин и пароль могут содержать только латинские буквы, цифры и знаки препинания.')

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT password_hash FROM users WHERE username=%s;", (username,))
        else:
            cur.execute("SELECT password_hash FROM users WHERE username=?;", (username,))

        user = cur.fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['login'] = username
            return redirect(url_for('rgz.profile_view'))  # Перенаправление на маршрут профиля
        else:
            return render_template('rgz/login.html', error='Неверный логин или пароль')
    finally:
        db_close(conn, cur)

@rgz.route('/api/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
    conn, cur = db_connect()
    try:
        if request.method == 'GET':
            username = session.get('login')
            if not username:
                return {'error': 'Unauthorized'}, 401
            
            # Получаем информацию о пользователе
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
            else:
                cur.execute("SELECT * FROM users WHERE username=?;", (username,))
                
            user = cur.fetchone()
            return {'user': user}, 200

        elif request.method == 'PUT':
            username = session.get('login')
            if not username:
                return {'error': 'Unauthorized'}, 401

            data = request.get_json()
            full_name = data.get('full_name')
            age = data.get('age')
            gender = data.get('gender')
            search_gender = data.get('search_gender')
            about = data.get('about')
            is_hidden = data.get('is_hidden', False)

            # Обновляем информацию о пользователе
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE users SET full_name=%s, age=%s, gender=%s, search_gender=%s, about=%s, is_hidden=%s
                    WHERE username=%s;
                """, (full_name, age, gender, search_gender, about, is_hidden, username))
            else:
                cur.execute("""
                    UPDATE users SET full_name=?, age=?, gender=?, search_gender=?, about=?, is_hidden=?
                    WHERE username=?;
                """, (full_name, age, gender, search_gender, about, is_hidden, username))

            conn.commit()
            return {'message': 'Profile updated successfully'}, 200

        elif request.method == 'DELETE':
            username = session.get('login')
            if not username:
                return {'error': 'Unauthorized'}, 401

            # Удаляем пользователя
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("DELETE FROM users WHERE username=%s;", (username,))
            else:
                cur.execute("DELETE FROM users WHERE username=?;", (username,))
                
            conn.commit()
            session.pop('login', None)  # Удаляем сессию
            return {'message': 'Account deleted successfully'}, 200

    finally:
        db_close(conn, cur)

@rgz.route('/rgz/profile', methods=['GET'])
def profile_view():
    username = session.get('login')
    if not username:
        return redirect(url_for('rgz.login'))  # Перенаправление на страницу входа, если пользователь не авторизован

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
        else:
            cur.execute("SELECT * FROM users WHERE username=?;", (username,))

        user = cur.fetchone()
        return render_template('rgz/profile.html', user=user)  # Отображаем профиль пользователя
    finally:
        db_close(conn, cur)


