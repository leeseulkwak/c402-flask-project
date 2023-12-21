
from flask import Blueprint, render_template, url_for, redirect
from my_app.models import Question

bp=Blueprint('main', __name__, url_prefix='/')


#홈화면
@bp.route('/')
def index():
    return render_template('index.html')

 