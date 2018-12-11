from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from ..forms import RegisterForm, LoginForm, ProfileForm, AvatarForm, PasswordForm, WalletForm
from ..services import TbUser, TbFile
from ..models import User

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('/register', methods=['GET', 'POST'])
def register():
    """注册用户
    """

    form = RegisterForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json('/users', json={
            'username': form.username.data,
            'password': form.password.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/register.html', form=form)

        flash('注册成功，请登录', 'success')
        return redirect(url_for('.login'))

    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    """登录
    """

    form = LoginForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).get_json('/users/check_password', params={
            'username': form.username.data,
            'password': form.password.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/login.html', form=form)
        if not resp['data']['isCorrect']:
            flash('用户名或密码错误')
            return render_template('user/login.html', form=form)

        login_user(User(resp['data']['user']), form.remember_me.data)

        return redirect(url_for('common.index'))

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    """退出
    """

    logout_user()
    flash('退出成功', 'success')
    return redirect(url_for('common.index'))


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json(
            '/users/{}'.format(current_user.get_id()), json={
                'username': form.username.data,
                'gender': form.gender.data,
                'mobile': form.mobile.data,
            }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/profile.html', form=form)

        return redirect(url_for('common.index'))

    return render_template('user/profile.html', form=form)


@user.route('/avatar', methods=['GET', 'POST'])
@login_required
def avatar():
    """设置头像
    """

    form = AvatarForm()
    if form.validate_on_submit():
        # 上传头像文件到文件服务，获得一个文件 ID
        f = form.avatar.data
        resp = TbFile(current_app).post_json('/files', files={
            'file': (secure_filename(f.filename), f, f.mimetype),
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/avatar.html', form=form)

        # 将前面获得的文件 ID 通过用户服务接口更新到用户资料里
        resp = TbUser(current_app).post_json(
            '/users/{}'.format(current_user.get_id()), json={
                'avatar': resp['data']['id'],
            }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/avatar.html', form=form)

        return redirect(url_for('common.index'))

    return render_template('user/avatar.html', form=form)


@user.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """修改密码
    """

    form = PasswordForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json(
            '/users/{}'.format(current_user.get_id()), json={
                'password': form.password.data,
            }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/password.html', form=form)

        return redirect(url_for('common.index'))

    return render_template('user/password.html', form=form)


@user.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    """钱包充值
    """

    form = WalletForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json(
            '/users/{}'.format(current_user.get_id()), json={
                'wallet_money': current_user.wallet_money + form.money.data,
            }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('user/wallet.html', form=form)

        flash('充值成功', 'info')
        return redirect(url_for('.wallet'))

    return render_template('user/wallet.html', form=form)


@user.route('/wallet_transactions')
@login_required
def wallet_transactions():
    """钱包交易记录
    """

    resp = TbUser(current_app).get_json('/wallet_transactions', params={
        'user_id': current_user.get_id(),
    })
    wallet_transactions = resp['data']['wallet_transactions']
    total = resp['data']['total']

    return render_template('user/wallet_transactions.html', wallet_transactions=wallet_transactions, total=total)
