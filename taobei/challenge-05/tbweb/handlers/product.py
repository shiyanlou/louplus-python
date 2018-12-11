from flask import Blueprint, request, current_app, render_template

from ..services import TbMall

product = Blueprint('product', __name__, url_prefix='/products')


@product.route('')
def index():
    """商品列表
    """

    keywords = request.args.get('keywords', '')
    page = request.args.get('page', 1, type=int)

    limit = current_app.config['PAGINATION_PER_PAGE']
    offset = (page - 1) * limit
    resp = TbMall(current_app).get_json('/products', params={
        'keywords': keywords,
        'limit': limit,
        'offset': offset
    })

    return render_template('product/index.html', **resp['data'], keywords=keywords)


@product.route('/<int:id>')
def detail(id):
    """商品详情
    """

    resp = TbMall(current_app).get_json('/products/{}'.format(id))
    return render_template('product/detail.html', **resp['data'])
