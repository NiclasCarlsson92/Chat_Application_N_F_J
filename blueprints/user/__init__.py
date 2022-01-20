from flask import Blueprint, render_template, redirect, url_for, request, flash

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/user')
def user_profile_get():
    return render_template('user_profile.html')
