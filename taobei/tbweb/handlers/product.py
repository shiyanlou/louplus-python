from flask import Blueprint, request, current_app, render_template

from ..services import TbMall

product = Blueprint('product', __name__, url_prefix='/products')


@product.route('')
def index():
    resp = TbMall(current_app).get_json('/products')
    return render_template('product/index.html', **resp['data'])
