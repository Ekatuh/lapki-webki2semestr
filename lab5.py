from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session
from functools import wraps
lab5 = Blueprint('lab5', __name__, static_folder='static')

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

