from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp_admin = Blueprint("bp_admin", __name__)


@bp_admin.before_request
def before_request():
    if not current_user.is_authenticated or not current_user.admin:
        return redirect(url_for("bp_home.home_get"))


@bp_admin.get("/admin")
def get_admin():
    return render_template("/admin.html")