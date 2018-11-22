from flask import Blueprint, request, current_app, render_template

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('')
def index():
    return render_template('user/index.html')
