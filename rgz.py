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
    photo_url = request.form.get('photo_url')  # Получаем URL фотографии

    # Валидация логина и пароля
    if not (username and password and full_name and age and gender and search_gender and photo_url):
        return render_template('rgz/register.html', error='Заполните все обязательные поля')

    if not is_valid_username_password(username) or not is_valid_username_password(password):
        return render_template('rgz/register.html', error='Логин и пароль могут содержать только латинские буквы, цифры и знаки препинания.')

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
            """, (username, password_hash, full_name, age, gender, search_gender, about, photo_url))
        else:
            cur.execute("""
                INSERT INTO users (username, password_hash, full_name, age, gender, search_gender, about, photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (username, password_hash, full_name, age, gender, search_gender, about, photo_url))

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

@rgz.route('/rgz/edit_profile', methods=['GET', 'POST'])
def edit_profile_view():
    username = session.get('login')
    if not username:
        return {'error': 'Unauthorized'}, 401

    if request.method == 'POST':
        data = request.get_json()  # Получаем данные JSON
        if not data:
            return {'error': 'Invalid JSON'}, 400  # Проверка на случай, если данные не были отправлены

        full_name = data.get('full_name')
        age = data.get('age')
        gender = data.get('gender')  
        search_gender = data.get('search_gender')  
        about = data.get('about')
        photo_url = data.get('photo_url')

        # Логика обновления профиля
        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE users 
                    SET full_name = %s, age = %s, gender = %s, search_gender = %s, about = %s, photo = %s 
                    WHERE username = %s;
                """, (full_name, age, gender, search_gender, about, photo_url, username))
            else:
                cur.execute("""
                    UPDATE users 
                    SET full_name = ?, age = ?, gender = ?, search_gender = ?, about = ?, photo = ? 
                    WHERE username = ?;
                """, (full_name, age, gender, search_gender, about, photo_url, username))

            conn.commit()
            return {'message': 'Profile updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500  # Возвращаем ошибку, если что-то пошло не так
        finally:
            db_close(conn, cur)

    # Если метод GET, отображаем форму редактирования
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
        else:
            cur.execute("SELECT * FROM users WHERE username=?;", (username,))

        user = cur.fetchone()
        return render_template('rgz/edit_profile.html', user=user)  # Отображение шаблона редактирования профиля
    finally:
        db_close(conn, cur)

@rgz.route('/api/hide_profile', methods=['POST'])
def hide_profile():
    username = session.get('login')
    if not username:
        return {'error': 'Unauthorized'}, 401

    conn, cur = db_connect()
    try:
        # Переключаем состояние видимости профиля
        cur.execute("UPDATE users SET is_hidden = NOT is_hidden WHERE username = %s;", (username,))
        conn.commit()
        return {'message': 'Profile visibility toggled successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500  # Возвращаем ошибку, если что-то пошло не так
    finally:
        db_close(conn, cur)

@rgz.route('/api/open_profile', methods=['POST'])
def open_profile():
    username = session.get('login')
    if not username:
        return {'error': 'Unauthorized'}, 401

    conn, cur = db_connect()
    try:
        cur.execute("UPDATE users SET is_hidden = FALSE WHERE username = %s;", (username,))
        conn.commit()
        return {'message': 'Profile opened successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500  # Возвращаем ошибку, если что-то пошло не так
    finally:
        db_close(conn, cur)

@rgz.route('/api/delete_account', methods=['DELETE'])
def delete_account():
    username = session.get('login')
    if not username:
        return {'error': 'Unauthorized'}, 401

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM users WHERE username = %s;", (username,))
        else:
            cur.execute("DELETE FROM users WHERE username = ?;", (username,))

        conn.commit()
        session.pop('login', None)  # Удаляем пользователя из сессии
        return {'message': 'Account deleted successfully'}, 200
    finally:
        db_close(conn, cur)

@rgz.route('/api/logout', methods=['POST'])
def logout():
    session.pop('login', None)  # Удаляем пользователя из сессии
    return {'message': 'Logged out successfully'}, 200

@rgz.route('/rgz/profile', methods=['GET'])
def profile_view():
    username = session.get('login')
    if not username:
        return redirect(url_for('rgz.login'))  # Перенаправление на страницу входа, если не авторизован

    # Логика получения информации о пользователе
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE username=%s;", (username,))
        else:
            cur.execute("SELECT * FROM users WHERE username=?;", (username,))

        user = cur.fetchone()
        return render_template('rgz/profile.html', user=user)  # Отображение шаблона профиля
    finally:
        db_close(conn, cur)

@rgz.route('/api/users', methods=['GET'])
def get_users():
    page = int(request.args.get('page', 1))
    limit = 3
    offset = (page - 1) * limit

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT full_name, username, age, photo, about FROM users LIMIT %s OFFSET %s;", (limit, offset))
        else:
            cur.execute("SELECT full_name, username, age, photo, about FROM users LIMIT ? OFFSET ?;", (limit, offset))

        users = cur.fetchall()
        return jsonify(users)

    finally:
        db_close(conn, cur)

@rgz.route('/rgz/users', methods=['GET'])
def list_users():
    conn, cur = db_connect()
    try:
        username = session.get('login')
        
        # Получаем информацию о текущем пользователе
        if username:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT gender, search_gender FROM users WHERE username=%s;", (username,))
            else:
                cur.execute("SELECT gender, search_gender FROM users WHERE username=?;", (username,))
                
            current_user = cur.fetchone()
            if current_user is None:
                return redirect(url_for('rgz.login'))  # Если пользователь не найден, перенаправляем на страницу входа

            current_gender = current_user['gender']
            search_gender = current_user['search_gender']
        else:
            return redirect(url_for('rgz.login'))  # Если пользователь не авторизован, перенаправляем на страницу входа

        # Получаем всех пользователей, исключая текущего, скрытых и фильтруем по полу
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT full_name, username, age, photo, about 
                FROM users 
                WHERE username != %s 
                AND is_hidden = FALSE
                AND gender = %s 
                AND search_gender = %s;
            """, (username, search_gender, current_gender))
        else:
            cur.execute("""
                SELECT full_name, username, age, photo, about 
                FROM users 
                WHERE username != ? 
                AND is_hidden = 0
                AND gender = ? 
                AND search_gender = ?;
            """, (username, search_gender, current_gender))

        users = cur.fetchall()  # Получаем всех пользователей, соответствующих критериям
        return render_template('rgz/user_list.html', users=users)

    finally:
        db_close(conn, cur)


