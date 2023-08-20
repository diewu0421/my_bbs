from flask_wtf.file import FileAllowed
from wtforms import StringField, ValidationError, BooleanField, FloatField, FileField, DecimalField

from wtforms.validators import input_required, length, data_required
from forms.baseforms import BaseForm


class GuaranteeForm(BaseForm):
    __tablename__ = "guarantee"
    gua_number = StringField(validators=[input_required(message="请输入保函编号")])
    amount = FloatField(validators=[input_required(message="请输入正确金额")])
    warrantee = StringField(validators=[input_required(message="请输入被保证人")])
    beneficiary = StringField(validators=[input_required(message="请输入受益人")])
    query_code = StringField(validators=[input_required(message="请输入保函查询码")])
    gua_pic = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="请选择正确类型的文件"), input_required(message="请选择文件")])
