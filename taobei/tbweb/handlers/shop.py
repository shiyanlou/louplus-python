from flask import Blueprint, request, current_app, render_template

from ..services import TbMall, TbUser

shop = Blueprint('shop', __name__, url_prefix='/shops')


@shop.route('')
def index():
    page = request.args.get('page', 1, type=int)

    limit = current_app.config['PAGINATION_PER_PAGE']
    offset = (page - 1) * limit
    resp = TbMall(current_app).get_json('/shops', params={
        'limit': limit,
        'offset': offset
    })
    shops = resp['data']['shops']
    total = resp['data']['total']

    user_ids = [shop['user_id'] for shop in shops]
    if len(user_ids) > 0:
        resp = TbUser(current_app).get_json('/users/infos', params={
            'ids': ','.join([str(v) for v in user_ids]),
        })
        for shop in shops:
            shop['user'] = resp['data']['users'].get(str(shop['user_id']))

    for shop in shops:
        r = TbMall(current_app).get_json('/products', params={
            'shop_id': shop['id'],
            'limit': 3
        })
        shop['products'] = r['data']['products']

    return render_template('shop/index.html', shops=shops, total=total)


@shop.route('/<int:id>')
def detail(id):
    page = request.args.get('page', 1, type=int)

    resp = TbMall(current_app).get_json('/shops/{}'.format(id))
    shop = resp['data']['shop']

    resp = TbUser(current_app).get_json('/users/{}'.format(id))
    shop['user'] = resp['data']['user']

    limit = current_app.config['PAGINATION_PER_PAGE']
    offset = (page - 1) * limit
    resp = TbMall(current_app).get_json('/products', params={
        'shop_id': id,
        'limit': limit,
        'offset': offset
    })

    return render_template('shop/detail.html', shop=shop, **resp['data'])
