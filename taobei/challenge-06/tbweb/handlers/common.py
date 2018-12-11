from flask import Blueprint, request, current_app, render_template, redirect

from tblib.redis import redis

from ..services import TbMall
from .shop import full_shop_info

common = Blueprint('common', __name__, url_prefix='/')


@common.route('')
def index():
    product_ids = [int(x) for x in redis.lrange('recommend.products', 0, 3)]

    resp = TbMall(current_app).get_json('/products/infos', params={
        'ids': ','.join([str(v) for v in product_ids]),
    })

    products = []
    for product_id in product_ids:
        product = resp['data']['products'].get(str(product_id))
        if product is not None:
            products.append(product)

    shop_ids = [int(x) for x in redis.lrange('recommend.shops', 0, 2)]

    resp = TbMall(current_app).get_json('/shops/infos', params={
        'ids': ','.join([str(v) for v in shop_ids]),
    })

    shops = []
    for shop_id in shop_ids:
        shop = resp['data']['shops'].get(str(shop_id))
        if shop is not None:
            shops.append(shop)

    shops = full_shop_info(shops)

    return render_template('index.html', products=products, shops=shops)
