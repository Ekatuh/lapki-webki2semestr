from flask import Flask, redirect, url_for

app = Flask(__name__, static_folder='static')

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head> 
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head> 
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""

@app.route ('/lab1/oak')
def oak():
    return'''
<!doctype html>
<html> 
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''"> 
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="'''+url_for('static', filename='oak.webp')+'''">
    </body>
</html>
'''  
