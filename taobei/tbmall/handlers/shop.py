from flask import Blueprint, request, current_app
from sqlalchemy import or_

from ..db import session
from ..models import Shop, ShopSchema, Product, ProductSchema
from .common import json_response, ResponseCode

shop = Blueprint('shop', __name__, url_prefix='/')


@shop.route('/shops', methods=['POST'])
def create_shop():
    shop = ShopSchema().load(request.get_json())

    session.add(shop)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/shops', methods=['GET'])
def shop_list():
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Shop.id.asc() if order_direction == 'asc' else Shop.id.desc()
    query = Shop.query.order_by(order_by).limit(limit).offset(offset)

    return json_response(shops=ShopSchema().dump(query, many=True))


@shop.route('/shops/<int:shop_id>', methods=['POST'])
def update_shop(shop_id):
    values = request.get_json()

    shop = Shop.query.get(shop_id)
    count = shop.update(values)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/shops/<int:shop_id>', methods=['GET'])
def shop_info(shop_id):
    shop = Shop.query.get(shop_id)
    if shop is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    shop = Shop.query.get(shop_id)
    count = shop.delete()
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/shops/<int:shop_id>/products', methods=['POST'])
def create_product_for_shop(shop_id):
    product = ProductSchema().load(request.get_json())

    shop = Shop.query.get(shop_id)
    if shop is None:
        return json_response(ResponseCode.NOT_FOUND)
    product.shops.append(shop)

    session.add(product)
    session.commit()

    return json_response(product=ProductSchema().dump(product))


@shop.route('/shops/<int:shop_id>/products', methods=['GET'])
def products_of_shop(shop_id):
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Product.id.asc() if order_direction == 'asc' else Product.id.desc()
    query = Shop.query.get(shop_id).products.order_by(
        order_by).limit(limit).offset(offset)

    return json_response(products=ProductSchema().dump(query, many=True))
