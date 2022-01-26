from flask import Blueprint, render_template, redirect, url_for, request

bp_dm = Blueprint('bp_dm', __name__)


@bp_dm.get('/')
def dm_get():
    return render_template('dm.html')
