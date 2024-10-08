from flask import Flask, redirect, url_for, render_template, render_template_string, abort, request

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
            <ul>
                <li><a href="/lab2">Вторая лабораторная</a></li>
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
        <p>НГТУ, ФБ, Лабораторная работа 1</p>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/menu">Меню</a>
        
        <h2>Реализованные роуты</h2>
        <nav>
            <ul>
                <li><a href="/lab1/oak">/lab1/oak-Дуб</a></li>
            </ul>
            <ul>
                <li><a href="/lab1/student">/lab1/student-Студент</a></li>
            </ul>
            <ul>
                <li><a href="/lab1/python">/lab1/python-Python</a></li>
            </ul>
            <ul>
                <li><a href="/lab1/book">/lab1/book-Книга</a></li>
            </ul>
        </nav>
        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route("/lab2")
def lab2_menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head> 
    <body>
        <p>НГТУ, ФБ, Лабораторная работа 2</p>
       
        <a href="/menu">Меню</a>
        
        <h2>Реализованные роуты</h2>
        <nav>
            <ul>
                <li><a href="/lab2/a">/lab2/a-Без слэша</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/a/">/lab2/a/-Со слэшем</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/flowers/<int:flower_id>">/lab2/flowers/<int:flower_id>-Цветы</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/example">/lab2/example-Настройки</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/filters">/lab2/filters-Фильтры</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/calc/">/lab2/calc/-Калькулятор</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/books">/lab2/books-Книги</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/objects">/lab2/objects-Ягоды</a></li>
            </ul>
            <ul>
                <li><a href="/lab2/flowers">/lab2/flowers-Цветы</a></li>
            </ul>
        </nav>
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

        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''  

@app.route ('/lab1/student')
def student():
    return'''
<!doctype html>
<html> 
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''"> 
    </head>
    <body>
        <h2>Кузьменко Екатерина Алексеевна</h2>
        <img src="'''+url_for('static', filename='Логотип_НГТУ_НЭТИ.png')+'''" style="width: 200px; height: auto;">

        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''  

@app.route ('/lab1/python')
def python():
    return'''
<!doctype html>
<html> 
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''"> 
    </head>
    <body>
        <p><b>Python — это скриптовый язык программирования.</b> Он универсален и подходит для решения разнообразных задач на разных
        платформах, включая iOS и Android, а также серверные операционные системы.</p>

        <p>Это интерпретируемый язык, а не компилируемый, как C++ или Java. Программа на Python представляет собой обычный 
        текстовый файл. Код можно писать практически в любом редакторе или использовать специальные IDE.</p>

        <p>Python используется в различных сферах, таких как веб-разработка, научные исследования и машинное обучение, тестирование, 
        создание десктопных и мобильных приложений, а также игр.</p>

        <img src="'''+url_for('static', filename='python.jpg')+'''" style="width: 400px; height: auto; display: block; margin: 20px auto;">

        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''  

@app.route ('/lab1/book')
def book():
    return'''
<!doctype html>
<html> 
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''"> 
    </head>
    <body>
        <p><i><b>«Портрет Дориана Грея»</b> (англ. The Picture of Dorian Gray)</i> — роман ирландского писателя и драматурга Оскара Уайльда.В 
        жанровом отношении представляет смесь романа воспитания с моральной притчей; оказался самым успешным произведением Уайльда, 
        экранизировался в разных странах мира более 30 раз. Существует в трёх версиях — журнальный вариант в тринадцати главах, 
        опубликованный в Lippincott’s Monthly Magazine в июле 1890 года, подвергшийся сокращениям, сделанным редактором журнала; 
        первое книжное издание в двадцати главах (апрель 1891 года), в которое автором были добавлены главы III, V, XV—XVIII, а 
        последняя глава разделена на две, ставшие главами XIX и XX[2][3] и «бесцензурная» версия романа в тринадцати главах, 
        представляющая собой первоначальную оригинальную машинопись Уайльда, впервые опубликованную в 2011 году Издательством 
        Гарвардского университета. В основе всех изданий на английском языке и переводов лежит книжная версия 1891 года.</p>

        <p>Художник Бэзил Холлуорд пишет портрет молодого и прекрасного Дориана Грея. Любуясь своим изображением, юноша выражает 
        желание, чтобы портрет старел, а он всегда оставался молодым. Дориан знакомится с другом Бэзила, лордом Генри Уоттоном — 
        саркастичным гедонистом, презирающим традиционные викторианские ценности, и попадает под влияние его порочных идей. Дориан 
        влюбляется в актрису, юную красавицу Сибилу Вэйн, но после провала спектакля, на который он пригласил лорда Генри и Бэзила, 
        он объявляет влюблённой в него актрисе о разрыве. Вернувшись домой, он обнаруживает, что в очертаниях губ на портрете появилась 
        складка жестокости, в то время сам Дориан не изменился. Он понимает, что повёл себя плохо, и решает жениться на Сибиле, но 
        лорд Генри сообщает, что она покончила жизнь самоубийством. Генри удаётся развеять сожаления Дориана.</p>

        <p>Спустя несколько лет Бэзил случайно встречает на улице Дориана и настаивает на беседе с ним. Бэзил рассказывает Дориану о 
        кошмарной репутации, которую тот приобрёл. Бэзил не верит рассказам о Дориане, он считает, что пороки человека неизбежно 
        отражаются на его внешности. Однако Дориан сохранил всю красоту своей молодости, что разрушает теорию Бэзила. Бэзил требует 
        откровенного ответа, на что Дориан показывает портрет, на котором изображён отталкивающий постаревший человек, на лице которого 
        отражены его пороки. Бэзил узнаёт свою работу и с ужасом осознаёт, что все слухи о Дориане — правда. Озлобленный Грей убивает 
        Холлуорда. Шантажируя своего бывшего друга учёного Кэмпбелла, Дориан заставляет его уничтожить труп.</p>

        <img src="'''+url_for('static', filename='Дориан.jpg')+'''" style="width: 400px; height: auto; display: block; margin: 20px auto;">

        <footer>
            &copy; Кузьменко Екатерина, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''  

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Роза", "price": 100},
    {"name": "Тюльпан", "price": 50},
    {"name": "Лилия", "price": 80}
]

@app.route('/lab2/flowers')
def list_flowers():
    return render_template_string('''
<!doctype html>
<html>
    <body>
        <h1>Список всех цветов</h1>
        <ol>
            {% for flower in flowers %}
                <li>
                    {{ flower.name }} - {{ flower.price }} руб.
                    <a href="{{ url_for('delete_flower', index=loop.index0) }}">Удалить</a>
                </li>
            {% endfor %}
        </ol>
        <p>Всего цветов: {{ count }}</p>
        <form action="{{ url_for('add_flower') }}" method="post">
            <input type="text" name="name" placeholder="Название цветка" required>
            <input type="number" name="price" placeholder="Цена цветка" required>
            <button type="submit">Добавить цветок</button>
        </form>
        <a href="{{ url_for('clear_flowers') }}">Очистить список цветов</a>
    </body>
</html>
''', flowers=flower_list, count=len(flower_list))

@app.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    price = request.form['price']
    flower_list.append({"name": name, "price": price})
    return redirect(url_for('list_flowers'))

@app.route('/lab2/delete_flower/<int:index>')
def delete_flower(index):
    if index < 0 or index >= len(flower_list):
        abort(404)
    flower_list.pop(index)
    return redirect(url_for('list_flowers'))

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('list_flowers'))


@app.route('/lab2/example')
def example():
    name, number, group, curs = 'Екатерина Кузьменко', 2, 'ФБИ-23', '3 курс'  
    fruits = [
        {'name': 'Яблоки', 'price': 100},
        {'name': 'Груши', 'price': 120},
        {'name': 'Апельсины', 'price': 80},
        {'name': 'Мандарины', 'price': 95},
        {'name': 'Манго', 'price': 321}
    ]
    return render_template('example.html', 
                            name=name, number=number, group=group, 
                            curs=curs, fruits=fruits)

@app.route('/lab2/')
def lab2 ():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

books = [
    {'author': 'Джон Гришэм', 'title': 'Время убивать', 'genre': 'Детектив', 'pages': 480},
    {'author': 'Стивен Кинг', 'title': 'Сияние', 'genre': 'Ужасы', 'pages': 451},
    {'author': 'Дэн Браун', 'title': 'Код да Винчи', 'genre': 'Триллеры', 'pages': 544},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и философский камень', 'genre': 'Фэнтези', 'pages': 309},
    {'author': 'Эрих Мария Ремарк', 'title': 'Три товарища', 'genre': 'Роман', 'pages': 384},
    {'author': 'Толстой Лев Николаевич', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
    {'author': 'Фрэнк Герберт', 'title': 'Дюна', 'genre': 'Научная фантастика', 'pages': 607},
    {'author': 'Артур Конан Дойл', 'title': 'Собака Баскервилей', 'genre': 'Детектив', 'pages': 256},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и Тайная комната', 'genre': 'Фэнтези', 'pages': 341},
    {'author': 'Оскар Уайльд', 'title': 'Портрет Дориана Грея', 'genre': 'Роман', 'pages': 320},
]

@app.route('/lab2/books')
def books_list():
    return render_template('books_list.html', books=books)

objects = [
    {
        'name': 'Яблоко',
        'image': '/static/apple.jpg',
        'description': 'Сочный и сладкий фрукт, богатый витаминами.'
    },
    {
        'name': 'Груша',
        'image': '/static/pear.jpg',
        'description': 'Сладкий и сочный фрукт с нежной мякотью.'
    },
    {
        'name': 'Вишня',
        'image': '/static/cherry.jpg',
        'description': 'Кислая, но очень вкусная ягода, любимая многими.'
    },
    {
        'name': 'Клубника',
        'image': '/static/strawberry.webp',
        'description': 'Сладкая и ароматная ягода, символ лета.'
    },
    {
        'name': 'Смородина',
        'image': '/static/currant.webp',
        'description': 'Кислая ягода, богатая витаминами C и P.'
    }
]

@app.route('/lab2/objects')
def show_objects():
    return render_template('objects.html', objects=objects)

