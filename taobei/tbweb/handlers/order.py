from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from tblib.handler import json_response, ResponseCode

from ..forms import OrderForm
from ..services import TbBuy, TbUser, TbMall

order = Blueprint('order', __name__, url_prefix='/orders')


@order.route('')
@login_required
def index():
    """当前用户的订单列表
    """

    page = request.args.get('page', 1, type=int)

    limit = current_app.config['PAGINATION_PER_PAGE']
    offset = (page - 1) * limit
    resp = TbBuy(current_app).get_json('/orders', params={
        'user_id': current_user.get_id(),
        'limit': limit,
        'offset': offset,
    })

    orders = resp['data']['orders']
    total = resp['data']['total']

    orders = full_order_info(orders)

    return render_template('order/index.html', orders=orders, total=total)


def full_order_info(orders):
    """查询多个订单的详细信息，尽可能使用批量查询来优化性能
    """

    address_ids = []
    product_ids = []
    for order in orders:
        address_ids.append(order['address_id'])
        product_ids.extend([v['product_id'] for v in order['order_products']])

    addresses = {}
    if len(address_ids) > 0:
        resp = TbUser(current_app).get_json('/addresses/infos', params={
            'ids': ','.join([str(v) for v in address_ids]),
        })
        addresses = resp['data']['addresses']

    products = {}
    if len(product_ids) > 0:
        resp = TbMall(current_app).get_json('/products/infos', params={
            'ids': ','.join([str(v) for v in product_ids]),
        })
        products = resp['data']['products']

    for order in orders:
        order['address'] = addresses.get(str(order['address_id']))
        for order_product in order['order_products']:
            order_product['product'] = products.get(
                str(order_product['product_id']))

    return orders


@order.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建订单
    """

    form = OrderForm()

    resp = TbUser(current_app).get_json('/addresses', params={
        'user_id': current_user.get_id(),
    })
    addresses = resp['data']['addresses']
    form.address_id.choices = [(str(v['id']), v['address']) for v in addresses]
    for addresse in addresses:
        if addresse['is_default']:
            form.address_id.data = str(addresse['id'])

    resp = TbBuy(current_app).get_json('/cart_products', params={
        'user_id': current_user.get_id(),
    })
    cart_products = resp['data']['cart_products']
    if len(cart_products) == 0:
        flash('购物车为空', 'danger')
        return redirect(url_for('cart_product.index'))

    resp = TbMall(current_app).get_json('/products/infos', params={
        'ids': ','.join([str(v['product_id']) for v in cart_products]),
    })
    for cart_product in cart_products:
        cart_product['product'] = resp['data']['products'].get(
            str(cart_product['product_id']))

    if form.validate_on_submit():
        # 检查商品数量是否足够
        for cart_product in cart_products:
            if cart_product['amount'] > cart_product['product']['amount']:
                flash('商品“{}”数量不足'.format(
                    cart_product['product']['title']), 'danger')
                return render_template('order/create.html', form=form, cart_products=cart_products)

        # 创建订单
        resp = TbBuy(current_app).post_json('/orders', json={
            'address_id': form.address_id.data,
            'note': form.note.data,
            'order_products': [
                {
                    'product_id': v['product_id'],
                    'amount': v['amount'],
                    'price': v['product']['price'],
                } for v in cart_products
            ],
            'user_id': current_user.get_id(),
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('order/create.html', form=form, cart_products=cart_products)

        # 扣除商品数量
        for cart_product in cart_products:
            resp = TbMall(current_app).post_json(
                '/products/{}'.format(cart_product['product_id']), json={
                    'amount': cart_product['product']['amount'] - cart_product['amount'],
                })
            if resp['code'] != 0:
                flash(resp['message'], 'danger')
                return render_template('order/create.html', form=form, cart_products=cart_products)

        # 清空购物车
        resp = TbBuy(current_app).delete_json('/cart_products', params={
            'user_id': current_user.get_id(),
        })
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('order/create.html', form=form, cart_products=cart_products)

        return redirect(url_for('.index'))

    return render_template('order/create.html', form=form, cart_products=cart_products)


@order.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    """订单详情
    """

    resp = TbBuy(current_app).get_json('/orders/{}'.format(id))
    order = resp['data']['order']
    form = OrderForm(data=order)

    resp = TbUser(current_app).get_json('/addresses', params={
        'user_id': current_user.get_id(),
    })
    form.address_id.choices = [(str(v['id']), v['address'])
                               for v in resp['data']['addresses']]

    resp = TbMall(current_app).get_json('/products/infos', params={
        'ids': ','.join([str(v['product_id']) for v in order['order_products']]),
    })
    for order_product in order['order_products']:
        order_product['product'] = resp['data']['products'].get(
            str(order_product['product_id']))

    if form.validate_on_submit():
        resp = TbBuy(current_app).post_json('/orders/{}'.format(id), json={
            'address_id': form.address_id.data,
            'note': form.note.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('order/detail.html', form=form, order=order)

        return redirect(url_for('.index'))

    return render_template('order/detail.html', form=form, order=order)


@order.route('/<int:id>/pay', methods=['POST'])
@login_required
def pay(id):
    """支付订单
    """

    resp = TbBuy(current_app).get_json('/orders/{}'.format(id))
    order = resp['data']['order']

    resp = TbUser(current_app).get_json('/users/{}'.format(order['user_id']))
    user = resp['data']['user']
    if user['wallet_money'] < order['pay_amount']:
        return json_response(ResponseCode.NO_ENOUGH_MONEY)

    resp = TbMall(current_app).get_json('/products/infos', params={
        'ids': ','.join([str(v['product_id']) for v in order['order_products']]),
    })
    products = resp['data']['products']

    # 对订单中的每个商品，创建一笔交易来完成订单创建者向商品店主的付款
    for order_product in order['order_products']:
        product = products.get(str(order_product['product_id']))
        resp = TbUser(current_app).post_json('/wallet_transactions', json={
            'amount': order_product['amount'] * order_product['price'],
            'note': '支付订单({})商品({})'.format(order['id'], product['id']),
            'payer_id': order['user_id'],
            'payee_id': product['shop']['user_id'],
        })
        if resp['code'] != 0:
            return json_response(resp['code'], resp['message'], **resp['data'])

    resp = TbBuy(current_app).post_json('/orders/{}'.format(id), json={
        'status': 'paied',
    })

    flash('支付成功', 'success')
    return json_response(resp['code'], resp['message'], **resp['data'])


@order.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    """取消订单
    """

    resp = TbBuy(current_app).post_json('/orders/{}'.format(id), json={
        'status': 'cancelled',
    })

    return json_response(resp['code'], resp['message'], **resp['data'])
