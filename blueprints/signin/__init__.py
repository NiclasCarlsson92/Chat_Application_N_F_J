from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user

bp_signin = Blueprint('bp_signin', __name__)

from models import User


@bp_signin.get('/login')
def signin_get():
    return render_template('signin.html')


@bp_signin.post('/login')
def signin_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Wrong email or password')
        redirect(url_for('bp_signin.signin_get'))

    login_user(user)
    return redirect(url_for('bp_dashboard.dashboard_get'))

