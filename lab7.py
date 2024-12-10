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

