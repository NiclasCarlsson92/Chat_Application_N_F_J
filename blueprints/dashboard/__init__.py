from flask import Blueprint, render_template, redirect, url_for, request, flash

bp_dashboard = Blueprint('bp_dashboard', __name__)


@bp_dashboard.get('/dashboard')
def dashboard_get():
    return render_template('dashboard.html')
