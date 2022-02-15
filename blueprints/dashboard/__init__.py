from flask import Blueprint, render_template, redirect, url_for

bp_dashboard = Blueprint('bp_dashboard', __name__)


@bp_dashboard.get('/dashboard')
def dashboard_get():
    return render_template('dashboard.html')


@bp_dashboard.post('/dashboard/enter_chat')
def dashboard_enter_chat():
    return redirect(url_for('bp_chatroom.chatroom_post'))