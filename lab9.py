from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, jsonify

lab9 = Blueprint('lab9', __name__, static_folder='static')

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')

@lab9.route('/lab9/name', methods=['GET', 'POST'])
def get_name():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.get_age', name=name))
    return render_template('lab9/name.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def get_age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.get_gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def get_gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.get_preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)\

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def get_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form.get('preference')
        return redirect(url_for('lab9.get_sub_preference', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/sub_preference', methods=['GET', 'POST'])
def get_sub_preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        sub_preference = request.form.get('sub_preference')
        return redirect(url_for('lab9.congratulation', name=name, age=age, gender=gender, preference=preference, sub_preference=sub_preference))
    return render_template('lab9/sub_preference.html', name=name, age=age, gender=gender, preference=preference)

@lab9.route('/lab9/congratulation', methods=['GET'])
def congratulation():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    sub_preference = request.args.get('sub_preference')

    # Логика для выбора поздравления и картинки
    if gender == 'male':
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным..."
        if preference == 'tasty':
            if sub_preference == 'sweet':
                gift = "Вот тебе подарок — мешочек конфет."
                image = "candies.jpg"  # Путь к картинке с конфетами
            else:
                gift = "Вот тебе подарок — пицца."
                image = "pizza.jpg"  # Путь к картинке с пиццей
        else:
            gift = "Вот тебе подарок — набор для рисования."
            image = "art_set.jpg"  # Путь к картинке с набором для рисования
    else:
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной..."
        if preference == 'tasty':
            if sub_preference == 'sweet':
                gift = "Вот тебе подарок — торт."
                image = "cake.jpg"  # Путь к картинке с тортом
            else:
                gift = "Вот тебе подарок — пицца."
                image = "pizza.jpg"  # Путь к картинке с салатом
        else:
            gift = "Вот тебе подарок — набор для творчества."
            image = "craft.jpg"  # Путь к картинке с набором для творчества

    return render_template('lab9/congratulation.html', greeting=greeting, gift=gift, image=image)
