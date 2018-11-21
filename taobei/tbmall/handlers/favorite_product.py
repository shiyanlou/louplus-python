from flask import Blueprint, request, current_app
from sqlalchemy import and_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import FavoriteProduct, FavoriteProductSchema

favorite_product = Blueprint('favorite_product', __name__, url_prefix='/')


@favorite_product.route('/favorite_products', methods=['POST'])
def create_favorite_product():
    data = request.get_json()

    favorite_product = FavoriteProductSchema().load(data)
    session.add(favorite_product)
    session.commit()

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))


@favorite_product.route('/favorite_products', methods=['GET'])
def favorite_product_list():
    user_id = request.args.get('user_id', 0, type=int)
    product_id = request.args.get('product_id', 0, type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = FavoriteProduct.id.asc(
    ) if order_direction == 'asc' else FavoriteProduct.id.desc()
    query = FavoriteProduct.query
    if user_id > 0:
        query = query.filter(FavoriteProduct.user_id == user_id)
    if product_id > 0:
        query = query.filter(FavoriteProduct.product_id == product_id)
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(favorite_products=FavoriteProductSchema().dump(query, many=True))


@favorite_product.route('/favorite_products/<int:user_id>/<int:product_id>', methods=['DELETE'])
def delete_favorite_product(user_id, product_id):
    favorite_product = FavoriteProduct.query.filter(and_(
        FavoriteProduct.user_id == user_id, FavoriteProduct.product_id == product_id)).first()
    if favorite_product is None:
        return json_response(ResponseCode.NOT_FOUND)
    session.delete(favorite_product)
    session.commit()

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))


@favorite_product.route('/favorite_products/<int:user_id>/<int:product_id>', methods=['GET'])
def favorite_product_info(user_id, product_id):
    favorite_product = FavoriteProduct.query.filter(and_(
        FavoriteProduct.user_id == user_id, FavoriteProduct.product_id == product_id)).first()
    if favorite_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))
