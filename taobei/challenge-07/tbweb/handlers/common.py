from flask import Blueprint, request, current_app, render_template, redirect


common = Blueprint('common', __name__, url_prefix='/')


@common.route('')
def index():
    return render_template('index.html')
