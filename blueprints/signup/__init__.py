from flask import Blueprint, render_template, redirect, url_for, request

bp_signup = Blueprint('bp_signup', __name__)
from models import User

@bp_signup.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_signup.post('/signup')
def signup_post():
    email = request.form.get('email')
    password = request.form['password']

    return redirect(url_for('bp_home.home_get'))
# Ska peka mot sidan för en lyckad inlogging
