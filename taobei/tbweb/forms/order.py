from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import Required, Optional, Length, Email, EqualTo, DataRequired, ValidationError, NumberRange


class OrderForm(FlaskForm):
    address_id = SelectField('收货地址', validators=[Required()])
    note = StringField('备注', validators=[Optional(), Length(1, 200)])
    submit = SubmitField('提交')
