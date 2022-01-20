from flask import Blueprint, render_template, redirect, url_for, request, flash

from werkzeug.security import generate_password_hash

bp_signup = Blueprint('bp_signup', __name__)

from models import User


@bp_signup.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_signup.post('/signup')
def signup_post():
    email = request.form.get('email')
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='sha256')

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address is already in use")
        return redirect(url_for('bp_signup.signup_get'))

    new_user = User(email=email, password=hashed_password)
    from app import db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('bp_dashboard.dashboard_get'))
# Ska peka mot sidan för en lyckad inlogging
