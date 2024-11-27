from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__, static_folder='static')

offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": ""})

def db_connect():

    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(dbname="webka", 
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

@lab6.route('/')
def home():
    return redirect(url_for('lab6.lab'))

@lab6.route('/lab6/')
def lab():
    username = session.get('login', '')
    return render_template('lab6/lab6.html', login=session.get('login'), username=username)


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1, 
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    if data['method'] == 'cancellation':  # Исправлено: 'methon' на 'method'
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You cannot cancel someone else\'s booking'
                        },
                        'id': id
                    }
                office['tenant'] = ''  # Освобождаем офис
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }

@lab6.route('/lab6/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab6/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab6/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Проверка на существование пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab6/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    # Добавление нового пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab6/success.html', login=login)


@lab6.route('/lab6/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab6/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab6/login.html', error="Заполните поля")

    conn, cur = db_connect()

    # Поиск пользователя в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab6/login.html', error='Логин и/или пароль неверны')

    session['login'] = login  # Сохранение логина в сессии
    db_close(conn, cur)
    return redirect(url_for('lab6.lab'))

@lab6.route('/lab6/logout')
def logout():
    session.pop('login', None)  # Remove login from session
    return redirect(url_for('lab6.lab'))