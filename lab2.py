from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request

lab2 = Blueprint('lab2',__name__, static_folder='static')

@lab2.route("/lab2")
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


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {"name": "Роза", "price": 100},
    {"name": "Тюльпан", "price": 50},
    {"name": "Лилия", "price": 80}
]


@lab2.route('/lab2/flowers')
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
                    <a href="{{ url_for('lab2.delete_flower', index=loop.index0) }}">Удалить</a>
                </li>
            {% endfor %}
        </ol>
        <p>Всего цветов: {{ count }}</p>
        <form action="{{ url_for('lab2.add_flower') }}" method="post">
            <input type="text" name="name" placeholder="Название цветка" required>
            <input type="number" name="price" placeholder="Цена цветка" required>
            <button type="submit">Добавить цветок</button>
        </form>
        <a href="{{ url_for('lab2.clear_flowers') }}">Очистить список цветов</a>
    </body>
</html>
''', flowers=flower_list, count=len(flower_list))


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
  name = request.form['name']
  price = request.form['price']
  flower_list.append({"name": name, "price": price})
  return redirect(url_for('lab2.list_flowers'))


@lab2.route('/lab2/delete_flower/<int:index>')
def delete_flower(index):
    if index < 0 or index >= len(flower_list):
        abort(404)
    flower_list.pop(index)
    return redirect(url_for('lab2.list_flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.list_flowers'))


@lab2.route('/lab2/example')
def example():
    name, number, group, curs = 'Екатерина Кузьменко', 2, 'ФБИ-23', '3 курс'  
    fruits = [
        {'name': 'Яблоки', 'price': 100},
        {'name': 'Груши', 'price': 120},
        {'name': 'Апельсины', 'price': 80},
        {'name': 'Мандарины', 'price': 95},
        {'name': 'Манго', 'price': 321}
    ]
    return render_template('lab2/example.html', 
                            name=name, number=number, group=group, 
                            curs=curs, fruits=fruits)


@lab2.route('/lab2/')
def lab ():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1)) 

@lab2.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(url_for('lab2.calc', a=a, b=1)) 

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('lab2/calc.html', a=a, b=b)


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


@lab2.route('/lab2/books')
def books_list():
    return render_template('lab2/books_list.html', books=books)

objects = [
    {
        'name': 'Яблоко',
        'image': '/static/lab2/apple.jpg',
        'description': 'Сочный и сладкий фрукт, богатый витаминами.'
    },
    {
        'name': 'Груша',
        'image': '/static/lab2/pear.jpg',
        'description': 'Сладкий и сочный фрукт с нежной мякотью.'
    },
    {
        'name': 'Вишня',
        'image': '/static/lab2/cherry.jpg',
        'description': 'Кислая, но очень вкусная ягода, любимая многими.'
    },
    {
        'name': 'Клубника',
        'image': '/static/lab2/strawberry.webp',
        'description': 'Сладкая и ароматная ягода, символ лета.'
    },
    {
        'name': 'Смородина',
        'image': '/static/lab2/currant.webp',
        'description': 'Кислая ягода, богатая витаминами C и P.'
    }
]


@lab2.route('/lab2/objects')
def show_objects():
    return render_template('lab2/objects.html', objects=objects)
