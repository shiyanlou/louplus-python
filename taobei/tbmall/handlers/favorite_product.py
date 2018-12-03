from flask import Blueprint, request, current_app
from sqlalchemy import and_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import FavoriteProduct, FavoriteProductSchema

favorite_product = Blueprint(
    'favorite_product', __name__, url_prefix='/favorite_products')


@favorite_product.route('', methods=['POST'])
def create_favorite_product():
    """收藏商品
    """

    data = request.get_json()

    favorite_product = FavoriteProductSchema().load(data)
    session.add(favorite_product)
    session.commit()

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))


@favorite_product.route('', methods=['GET'])
def favorite_product_list():
    """收藏的商品列表，可根据用户 ID 和商品 ID 筛选
    """

    user_id = request.args.get('user_id', type=int)
    product_id = request.args.get('product_id', type=int)
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = FavoriteProduct.id.asc(
    ) if order_direction == 'asc' else FavoriteProduct.id.desc()
    query = FavoriteProduct.query
    if user_id is not None:
        query = query.filter(FavoriteProduct.user_id == user_id)
    if product_id is not None:
        query = query.filter(FavoriteProduct.product_id == product_id)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(favorite_products=FavoriteProductSchema().dump(query, many=True), total=total)


@favorite_product.route('/<int:id>', methods=['DELETE'])
def delete_favorite_product(id):
    """取消收藏商品
    """

    favorite_product = FavoriteProduct.query.get(id)
    if favorite_product is None:
        return json_response(ResponseCode.NOT_FOUND)
    session.delete(favorite_product)
    session.commit()

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))


@favorite_product.route('/<int:id>', methods=['GET'])
def favorite_product_info(id):
    """查询收藏商品
    """

    favorite_product = FavoriteProduct.query.get(id)
    if favorite_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(favorite_product=FavoriteProductSchema().dump(favorite_product))
