from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Product, ProductSchema, Shop, ShopSchema

product = Blueprint('product', __name__, url_prefix='/')


@product.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    product = ProductSchema().load(data)
    session.add(product)
    session.commit()

    return json_response(product=ProductSchema().dump(product))


@product.route('/products', methods=['GET'])
def product_list():
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Product.id.asc() if order_direction == 'asc' else Product.id.desc()
    query = Product.query.order_by(order_by).limit(limit).offset(offset)

    return json_response(products=ProductSchema().dump(query, many=True))


@product.route('/products/<int:product_id>', methods=['POST'])
def update_product(product_id):
    data = request.get_json()

    count = Product.query.filter(Product.id == product_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    product = Product.query.get(product_id)
    session.commit()

    return json_response(product=ProductSchema().dump(product))


@product.route('/products/<int:product_id>', methods=['GET'])
def product_info(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(product=ProductSchema().dump(product))


@product.route('/products/<int:product_id>/shops', methods=['POST'])
def add_shop_to_product(product_id):
    data = request.get_json()

    product = Product.query.get(product_id)
    if product is None:
        return json_response(ResponseCode.NOT_FOUND)
    product.shops.append(Shop.query.get(data['id']))
    session.commit()

    return json_response(product=ProductSchema().dump(product))


@product.route('/products/<int:product_id>/shops', methods=['GET'])
def shops_of_product(product_id):
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Shop.id.asc() if order_direction == 'asc' else Shop.id.desc()
    query = Product.query.get(product_id).shops.order_by(
        order_by).limit(limit).offset(offset)

    return json_response(shops=ShopSchema().dump(query, many=True))
