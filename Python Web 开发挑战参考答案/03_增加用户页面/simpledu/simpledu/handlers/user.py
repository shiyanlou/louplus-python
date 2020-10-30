from flask import Blueprint, render_template

from ..models import User


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
def detail(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user/detail.html', user=user)
