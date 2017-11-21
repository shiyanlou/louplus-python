from flask import Blueprint, render_template

front = Blueprint('front', __name__, url_prefix='/')


@front.route('/')
def index():
    return render_template('index.html')
