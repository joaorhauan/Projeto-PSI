from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('user_bp.login'))