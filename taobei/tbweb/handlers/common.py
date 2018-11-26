from flask import Blueprint, request, current_app, render_template, redirect


common = Blueprint('common', __name__, url_prefix='/')


@common.route('')
def index():
    return redirect('/products')


@common.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
