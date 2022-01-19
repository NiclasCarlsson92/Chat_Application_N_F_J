from flask import Blueprint, render_template, redirect, url_for, request

bp_login = Blueprint('bp_login', __name__)


@bp_login.get('/login')
def login_get():
    return render_template('login.html')
