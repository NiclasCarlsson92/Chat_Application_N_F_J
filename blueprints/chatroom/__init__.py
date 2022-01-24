from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user

bp_chatroom = Blueprint('bp_chatroom', __name__)

from models import User


@bp_chatroom.get('/chatroom')
def chatroom_get():
    return render_template('chatroom.html')


@bp_chatroom.post('/chatroom')
def chatroom_post():
    return redirect(url_for('bp_chatroom.chatroom_get'))
