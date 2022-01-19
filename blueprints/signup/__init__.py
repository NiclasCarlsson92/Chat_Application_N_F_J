from flask import Blueprint, render_template, redirect, url_for, request

bp_signup = Blueprint('bp_signup', __name__)


@bp_signup.get('/signup')
def signup_get():
    return render_template('signup.html')
