from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path


lab7 = Blueprint('lab7', __name__, static_folder='static')

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Harry Potter and the Prisoner of Azkaban",
        "title_ru": "Гарри Поттер и узник Азкабана",
        "year": 2004,
        "description": "Гарри, Рон и Гермиона возвращаются на третий курс школы чародейства и волшебства Хогвартс. На этот раз они должны раскрыть тайну узника, сбежавшего из тюрьмы Азкабан, чье пребывание на воле создает для Гарри смертельную опасность."
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "title_ru": "Гарри Поттер и философский камень",
        "year": 2001,
        "description": "Жизнь десятилетнего Гарри Поттера нельзя назвать сладкой: родители умерли, едва ему исполнился год, а от дяди и тёти, взявших сироту на воспитание, достаются лишь тычки да подзатыльники. Но в одиннадцатый день рождения Гарри всё меняется. Странный гость, неожиданно появившийся на пороге, приносит письмо, из которого мальчик узнаёт, что на самом деле он - волшебник и зачислен в школу магии под названием Хогвартс. А уже через пару недель Гарри будет мчаться в поезде Хогвартс-экспресс навстречу новой жизни, где его ждут невероятные приключения, верные друзья и самое главное — ключ к разгадке тайны смерти его родителей."
    },
    {
        "title": "Harry Potter and the Order of the Phoenix",
        "title_ru": "Гарри Поттер и Орден Феникса",
        "year": 2007,
        "description": "Гарри проводит свой пятый год в школе Хогвартс и обнаруживает, что многие из членов волшебного сообщества отрицают факт недавнего состязания юного волшебника с воплощением вселенского зла Волдемортом. Все делают вид, что не имеют ни малейшего представления, что злодей вернулся. Однако впереди волшебников ждет необычная схватка."
    },
    {
        "title": "Harry Potter and the Chamber of Secrets",
        "title_ru": "Гарри Поттер и Тайная комната",
        "year": 2002,
        "description": "Гарри Поттер переходит на второй курс Школы чародейства и волшебства Хогвартс. Эльф Добби предупреждает Гарри об опасности, которая поджидает его там, и просит больше не возвращаться в школу. Юный волшебник не следует совету эльфа и становится свидетелем таинственных событий, разворачивающихся в Хогвартсе. Вскоре Гарри и его друзья узнают о существовании Тайной Комнаты и сталкиваются с новыми приключениями, пытаясь победить темные силы."
    },
    {
        "title": "Harry Potter and the Goblet of Fire",
        "title_ru": "Гарри Поттер и Кубок огня",
        "year": 2005,
        "description": "Гарри Поттер, Рон и Гермиона возвращаются на четвёртый курс школы чародейства и волшебства Хогвартс. При таинственных обстоятельствах Гарри был отобран в число участников опасного соревнования — Турнира Трёх Волшебников, однако проблема в том, что все его соперники — намного старше и сильнее. К тому же, знаки указывают на возвращение Лорда Волдеморта. Вскоре Гарри предстоит побороться не только за победу в соревновании, но и за свою жизнь."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])  # Исправлено на 'films'
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])  # Исправлено на 'films'
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])  # Исправлено на 'films'
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)  
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])  # Исправлено на 'films'
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)  
    film = request.get_json()
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])  # Исправлено на 'films'
def add_film():
    film = request.get_json() 
    films.append(film)  
    return {'id': len(films) - 1}, 201
