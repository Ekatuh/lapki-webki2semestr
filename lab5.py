from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session
from functools import wraps
import psycopg2
lab5 = Blueprint('lab5', __name__, static_folder='static')

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = psycopg2.connect(
        dbname="webka", 
        user="postgres", 
        password="katya9056", 
        host="127.0.0.1"
    )

    cur = conn.cursor()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)


    