from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session
lab4 = Blueprint('lab4', __name__, static_folder='static')

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')
    