from flask import Blueprint, render_template, redirect, url_for, request

bp_home = Blueprint('bp_home', __name__)


@bp_home.get('/')
def home_get():
    return render_template('home.html')
