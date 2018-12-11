from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import Required, Optional, Length, Email, EqualTo, DataRequired, ValidationError, NumberRange


class CartProductForm(FlaskForm):
    product_id = HiddenField('商品', validators=[Required()])
    amount = IntegerField('购买数量', validators=[Required(), NumberRange(1, 100)])
    submit = SubmitField('提交')
