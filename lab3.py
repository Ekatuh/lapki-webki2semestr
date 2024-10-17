from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session

lab3 = Blueprint('lab3', __name__, static_folder='static')


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if name is None:
        name = "аноним"

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)



@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    

    errors2 = {}
    age = request.args.get('age')
    if age == '' or not age.isdigit(): 
        errors2['age'] = 'Заполните поле!' 

    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors, errors2=errors2)


@lab3.route('/lab3/order')
def order():
    return render_template ('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template ('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template ('lab3/success.html', price=price)


@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        background = request.form.get('background')
        size = request.form.get('size')
        font_style = request.form.get('font-style')

        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if size:
            resp.set_cookie('size', size)
        if font_style: 
            resp.set_cookie('font-style', font_style)

        return resp
    if request.method == 'DELETE':
        resp = make_response(redirect('/lab3/settings'))
        resp.delete_cookie('color')
        resp.delete_cookie('background')
        resp.delete_cookie('size')
        resp.delete_cookie('font-style')
        return resp

    background = request.cookies.get('background')
    color = request.cookies.get('color')
    size = request.cookies.get('size')
    font_style = request.cookies.get('font-style')

    return make_response(render_template('lab3/settings.html', color=color, 
                                         background=background, size=size, font_style=font_style))

@lab3.route('/lab3/clear_cookies', methods=['POST'])
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background')
    resp.delete_cookie('size')
    resp.delete_cookie('font-style')
    return resp


@lab3.route('/lab3/bilet', methods=['GET', 'POST'])
def bilet():
    if request.method == 'POST':
        
        fio = request.form['fio']
        polka = request.form['polka']
        belyo = request.form.get('belyo')
        bagazh = request.form.get('bagazh')
        vozrast = int(request.form['vozrast'])
        punkt_vyezda = request.form['punkt_vyezda']
        punkt_naznacheniya = request.form['punkt_naznacheniya']
        data_poezdki = request.form['data_poezdki']
        strahovka = request.form.get('strahovka')

        if not all([fio, polka, vozrast, punkt_vyezda, punkt_naznacheniya, data_poezdki]):
            return render_template('lab3/bilet.html', error='Заполните все поля!')
        if vozrast < 1 or vozrast > 120:
            return render_template('lab3/bilet.html', error='Некорректный возраст!')

        cena = 1000 if vozrast >= 18 else 700
        if polka in ('нижняя', 'нижняя боковая'):
            cena += 100
        if belyo:
            cena += 75
        if bagazh:
            cena += 250
        if strahovka:
            cena += 150

        
        return render_template('lab3/ofrmbilet.html', fio=fio, polka=polka, belyo=belyo, bagazh=bagazh, vozrast=vozrast, 
                               punkt_vyezda=punkt_vyezda, punkt_naznacheniya=punkt_naznacheniya, 
                               data_poezdki=data_poezdki, strahovka=strahovka, cena=cena)

    else:
        return render_template('lab3/bilet.html')

@lab3.route('/lab3/ofrmbilet')
def ofrmbilet():
    return render_template('lab3/ofrmbilet.html')

products = [
    {'name': 'Шоколад "Хрустящие печенье"', 'price': 250, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Пралине"', 'price': 210, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Мята"', 'price': 150, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Лесной орех"', 'price': 230, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Какао-мусс"', 'price': 120, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Карамельный мусс"', 'price': 110, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Клубника с йогуртом"', 'price': 160, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Марципан"', 'price': 155, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Клубника и мята"', 'price': 190, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Соленый миндаль и мёд"', 'price': 300, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Лимон и йогурт"', 'price': 270, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Кофе гляссе"', 'price': 180, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Молочный шоколад"', 'price': 100, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Темный шоколаад"', 'price': 90, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Белый шоколлад"', 'price': 136, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Цельный миндаль"', 'price': 170, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Кокос"', 'price': 173, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Ром, изюм, орех"', 'price': 137, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад "Карамельный мусс"', 'price': 179, 'brand': 'Ritter Sport', 'weight': '100g'},
    {'name': 'Шоколад " Крем-брюле"', 'price': 215, 'brand': 'Ritter Sport', 'weight': '100g'},
]

@lab3.route('/lab3/chocalete', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        min_price = request.form.get('min_price', type=float)
        max_price = request.form.get('max_price', type=float)
        
        filtered_products = [product for product in products if min_price <= product['price'] <= max_price]
        return render_template('lab3/results.html', products=filtered_products)

    return render_template('lab3/search.html')