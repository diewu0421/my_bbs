from wtforms import StringField, ValidationError, BooleanField, FloatField
from wtforms.validators import email, length, equal_to

from exts import cache
from forms.baseforms import BaseForm
from models.user import UserModel


class RegisterForm(BaseForm):
    email = StringField(validators=[email(message="请输入正确的邮箱地址！！！")])
    captcha = StringField(validators=[length(min=4, max=4, message="请输入验证码")])
    username = StringField(validators=[length(min=2, max=20, message="请输入用户名")])
    password = StringField(validators=[length(min=6, max=20, message="请输入密码")])
    confirm_password = StringField(validators=[equal_to(fieldname="password", message="密码不一致")])

    def validate_email(self, field):
        email = field.data
        query_email = UserModel.query.filter_by(email=email).first()
        if query_email:
            raise ValidationError("邮箱已存在")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or cache_captcha != captcha:
            raise ValidationError("验证码错误")


class LoginForm(BaseForm):
    email = StringField(validators=[email(message="请输入正确的邮箱")])
    password = StringField(validators=[length(min=6, max=20, message="请输入密码")])
    remember = BooleanField()
