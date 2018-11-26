from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from ..forms import RegisterForm, LoginForm
from ..services import TbUser
from ..models import User

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('.login'))
    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).get_json('/users', params={
            'username': form.username.data,
        })
        user = User(resp['data']['users'][0])
        login_user(user, form.remember_me.data)
        return redirect(url_for('common.index'))
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for('common.index'))
