from flask import Blueprint, render_template, redirect, url_for, request

bp_signin = Blueprint('bp_signin', __name__)


@bp_signin.get('/login')
def signin_get():
    return render_template('signin.html')


@bp_signin.post('/login')
def signin_post():
    return redirect(url_for('bp_dashboard.dashboard_get'))
