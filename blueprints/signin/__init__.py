from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user

from models import User
from passlib.hash import argon2

bp_signin = Blueprint('bp_signin', __name__)


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
        return redirect(url_for('bp_signin.signin_get'))

    if not argon2.verify(password, user.password):
        flash('Wrong email or password')
        return redirect(url_for('bp_signin.signin_get'))

    login_user(user)
    user.online = True

    from app import db
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('bp_dashboard.dashboard_get'))

