from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session
lab4 = Blueprint('lab4', __name__, static_folder='static')

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('/lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
  return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
  x1 = request.form.get('x1')
  x2 = request.form.get('x2')
  x1 = int(x1) if x1 else 0
  x2 = int(x2) if x2 else 0
  result = x1 + x2
  return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
  return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
  x1 = request.form.get('x1')
  x2 = request.form.get('x2')
  x1 = int(x1) if x1 else 1
  x2 = int(x2) if x2 else 1
  result = x1 * x2
  return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
  return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
  x1 = request.form.get('x1')
  x2 = request.form.get('x2')
  if x1 == '' or x2 == '':
    return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
  x1 = int(x1)
  x2 = int(x2)
  result = x1 - x2
  return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
  return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
  x1 = request.form.get('x1')
  x2 = request.form.get('x2')
  if x1 == '' or x2 == '':
    return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
  if x1 == '0' and x2 == '0':
    return render_template('lab4/pow.html', error='Нельзя возвести 0 в степень 0!')
  x1 = int(x1)
  x2 = int(x2)
  result = x1 ** x2
  return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1 
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1
    
    return redirect('/lab4/tree')



users = [
  {'login': 'alex', 'password': '123'},
  {'login': 'bob', 'password': '555'},
  {'login': 'ekatushka', 'password': '666'},
  {'login': 'dashushka', 'password': '69'},
]
@lab4.route('/lab4/login', methods= ['GET', 'POST'])
def login():
  if request.method == 'GET':
    if 'login' in session:
      authorized = True
      login = session['login']
    else:
      authorized = False
      login = ''
    return render_template ('lab4/login.html', authorized=authorized, login=login)

  login = request.form.get('login')
  password = request.form.get('password')

  for user in users:
    if login == user['login'] and password == user['password'] :
      session['login'] = login
      return redirect ('/lab4/login')

  error = 'Неверные логин и/или пароль'
  return render_template('lab4/login.html', error=error, authorized=False)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
  session.pop('login', None)
  return redirect('/lab4/login')


# Список пользователей с именем, полом, логином и паролем
users = [
    {"name": "Иван Иванов", "gender": "Мужской", "login": "ivan", "password": "123"},
    {"name": "Александра Петрова", "gender": "Женский", "login": "alexandra", "password": "555"},
]

@lab4.route('/lab4/auto', methods=['GET', 'POST'])
def auto():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if not login:
            error = "Не введён логин"
        elif not password:
            error = "Не введён пароль"
        else:
            user = next((u for u in users if u['login'] == login and u['password'] == password), None)
            if user:
                session['username'] = user['name']
                return redirect(url_for('lab4.welcome'))
            else:
                error = "Неверный логин или пароль"
        if error:
            return render_template('lab4/auto.html', error=error, login=login)
    return render_template('lab4/auto.html')

@lab4.route('/lab4/welcome')
def welcome():
    if 'username' in session:
        return f'Добро пожаловать, {session["username"]}'
    else:
        return redirect(url_for('lab4.auto'))

@lab4.route('/lab4/log')
def log():
    session.pop('username', None)
    return redirect(url_for('lab4.auto'))