from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request

lab3 = Blueprint('lab3', __name__, static_folder='static')

@lab3.route('/lab3/')
def lab():
  return render_template('lab3/lab3.html') 
