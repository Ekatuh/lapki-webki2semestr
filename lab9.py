from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, jsonify

lab9 = Blueprint('lab9', __name__, static_folder='static')

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')


