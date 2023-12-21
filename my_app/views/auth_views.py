from flask import Blueprint, request, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from my_app import db
from my_app.forms import UserCreateForm, UserLoginForm, UserForm
from my_app.models import User, Form
from datetime import datetime

import functools

bp=Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form=UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            user=User(username=form.username.data,
                      password=generate_password_hash(form.password1.data),
                      email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form=UserLoginForm()
    if request.method=='POST' and form.validate_on_submit():
        error=None
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            error="존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error="비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id']=user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

#폼화면
@bp.route('/form')
def form():
    return render_template('auth/FormPage.html')

#폼디비저장##

@bp.route('/view', methods=['GET', 'POST'])
def view():
    form=UserForm()
    if request.method=='POST':

        form_user=Form(firstname=form.firstname.data, lastname=form.lastname.data, cars=form.cars.data, 
                        fav_language=form.fav_language.data, create_date=datetime.now())
        
        
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        cars=request.form.get("cars")
        fav_language=request.form.get("fav_language")
        create_date=request.form.get("create_date")
        
        db.session.add(form_user)
        db.session.commit()
        return render_template('auth/FormView.html', firstname=firstname, lastname=lastname, cars=cars, fav_language=fav_language, create_date=create_date)

