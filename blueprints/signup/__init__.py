from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from passlib.hash import argon2
from models import User

bp_signup = Blueprint('bp_signup', __name__)


@bp_signup.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_signup.post('/signup')
def signup_post():
    name = request.form['username']
    email = request.form.get('email')
    password = request.form['password']
    hashed_password = argon2.using(rounds=10).hash(password)

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address is already in use")
        return redirect(url_for('bp_signup.signup_get'))

    new_user = User(name=name, email=email, password=hashed_password)

    from app import db
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for('bp_dashboard.dashboard_get'))
