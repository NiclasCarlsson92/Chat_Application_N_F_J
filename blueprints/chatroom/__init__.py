from flask import Blueprint, render_template, redirect, url_for

bp_chatroom = Blueprint('bp_chatroom', __name__)


@bp_chatroom.get('/chatroom')
def chatroom_get():
    return render_template('chatroom.html')


@bp_chatroom.post('/chatroom')
def chatroom_post():
    return redirect(url_for('bp_chatroom.chatroom_get'))
