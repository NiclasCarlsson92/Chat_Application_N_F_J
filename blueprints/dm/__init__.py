from flask import Blueprint, render_template

from controllers.user_controller import get_all_but_current_users

bp_dm = Blueprint('bp_dm', __name__)


@bp_dm.get('/dm')
def dm_get():
    users = get_all_but_current_users()
    return render_template('dm.html', users=users)
