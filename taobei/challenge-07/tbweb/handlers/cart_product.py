from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from tblib.handler import json_response

from ..services import TbBuy, TbMall
from ..forms import CartProductForm

cart_product = Blueprint('cart_product', __name__, url_prefix='/cart_products')


@cart_product.route('')
@login_required
def index():
    """购物车商品列表
    """

    resp = TbBuy(current_app).get_json('/cart_products', params={
        'user_id': current_user.get_id(),
    })
    cart_products = resp['data']['cart_products']
    total = resp['data']['total']

    product_ids = [cart_product['product_id']
                   for cart_product in cart_products]
    if len(product_ids) > 0:
        resp = TbMall(current_app).get_json('/products/infos', params={
            'ids': ','.join([str(v) for v in product_ids]),
        })
        for cart_product in cart_products:
            cart_product['product'] = resp['data']['products'].get(
                str(cart_product['product_id']))

    return render_template('cart_product/index.html', cart_products=cart_products, total=total)


@cart_product.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    """购物车商品详情
    """

    resp = TbBuy(current_app).get_json('/cart_products/{}'.format(id))
    cart_product = resp['data']['cart_product']

    resp = TbMall(current_app).get_json(
        '/products/{}'.format(cart_product['product_id']))
    product = resp['data']['product']

    form = CartProductForm(data=cart_product)
    if form.validate_on_submit():
        resp = TbBuy(current_app).post_json('/cart_products/{}'.format(cart_product['id']), json={
            'product_id': form.product_id.data,
            'amount': form.amount.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('cart_product/detail.html', form=form, product=product)

        return redirect(url_for('.index'))

    return render_template('cart_product/detail.html', form=form, product=product)


@cart_product.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    """删除购物车商品
    """

    resp = TbBuy(current_app).delete_json('/cart_products/{}'.format(id))

    return json_response(resp['code'], resp['message'], **resp['data'])


@cart_product.route('/add/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add(product_id):
    """添加商品到购物车
    """

    resp = TbMall(current_app).get_json('/products/{}'.format(product_id))
    product = resp['data']['product']

    form = CartProductForm(data={
        'product_id': product_id,
        'amount': 1,
    })
    if form.validate_on_submit():
        resp = TbBuy(current_app).post_json('/cart_products', json={
            'user_id': current_user.get_id(),
            'product_id': form.product_id.data,
            'amount': form.amount.data,
        }, check_code=False)
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('cart_product/add.html', form=form, product=product)

        return redirect(url_for('.index'))

    return render_template('cart_product/add.html', form=form, product=product)
