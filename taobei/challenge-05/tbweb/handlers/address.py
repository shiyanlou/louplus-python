from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from ..forms import AddressForm
from ..services import TbUser

address = Blueprint('address', __name__, url_prefix='/addresses')


@address.route('')
@login_required
def index():
    """当前用户地址列表
    """

    resp = TbUser(current_app).get_json('/addresses', params={
        'user_id': current_user.get_id(),
    })
    return render_template('address/index.html', addresses=resp['data']['addresses'])


@address.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """添加地址
    """

    form = AddressForm()
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json('/addresses', json={
            'address': form.address.data,
            'phone': form.phone.data,
            'zip_code': form.zip_code.data,
            'is_default': form.is_default.data,
            'user_id': current_user.get_id(),
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('address/create.html', form=form)

        return redirect(url_for('.index'))

    return render_template('address/create.html', form=form)


@address.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    """地址详情
    """

    resp = TbUser(current_app).get_json('/addresses/{}'.format(id))
    form = AddressForm(data=resp['data']['address'])
    if form.validate_on_submit():
        resp = TbUser(current_app).post_json('/addresses/{}'.format(id), json={
            'address': form.address.data,
            'phone': form.phone.data,
            'zip_code': form.zip_code.data,
            'is_default': form.is_default.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('address/detail.html', form=form)

        return redirect(url_for('.index'))

    return render_template('address/detail.html', form=form)
