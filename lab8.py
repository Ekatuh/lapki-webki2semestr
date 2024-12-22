from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, jsonify
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
from datetime import datetime


lab8 = Blueprint('lab8', __name__, static_folder='static')

@lab8.route('/lab8/')
def lab():
  username = session.get('login', '')
  return render_template('lab8/lab8.html', login=session.get('login'), username=username)