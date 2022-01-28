from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, login_required, current_user

from controllers.user_controller import get_user_by_id

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/user')
@login_required
def user_get():
    return render_template('user_profile.html')


@bp_user.get('/logout')
def logout_get():
    user = current_user
    user.online = False

    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_home.home_get'))


@bp_user.get("/message/<user_id>")
def message_get(user_id):
    user_id = int(user_id)
    reciver = get_user_by_id(user_id)
    return render_template("message.html", reciver=reciver)
