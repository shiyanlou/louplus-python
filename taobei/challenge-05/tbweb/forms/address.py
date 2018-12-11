from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Required, Optional, Length, Email, EqualTo, DataRequired, ValidationError, NumberRange


class AddressForm(FlaskForm):
    address = StringField('地址', validators=[Required(), Length(5, 50)])
    phone = StringField('联系电话', validators=[Required(), Length(5, 20)])
    zip_code = StringField('邮编', validators=[Optional(), Length(6, 6)])
    is_default = BooleanField('默认地址')
    submit = SubmitField('提交')
