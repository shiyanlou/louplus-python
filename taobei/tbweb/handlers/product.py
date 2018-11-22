from flask import Blueprint, request, current_app, render_template

from ..services import TbMall

product = Blueprint('product', __name__, url_prefix='/products')


@product.route('')
def index():
    products = TbMall(current_app).get('/products')
    return render_template('product/index.html')
