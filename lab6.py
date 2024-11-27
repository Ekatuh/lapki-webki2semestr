from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__, static_folder='static')

@lab6.route('/lab6/')
def lab():
  username = session.get('login', '')
  return render_template('lab6/lab6.html', login=session.get('login'), username=username)
