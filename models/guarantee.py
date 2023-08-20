from exts import db


class GuaranteeModel(db.Model):
    __tablename__ = 'guarantee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 保函编号
    gua_number = db.Column(db.String(50), nullable=False)
    # 金额
    amount = db.Column(db.Float, nullable=False)
    # 被保证人
    warrantee = db.Column(db.String(50), nullable=False)
    # 受益人
    beneficiary = db.Column(db.String(50), nullable=False)
    # 查询码
    query_code = db.Column(db.String(50), nullable=False)
    # 保函图片
    gua_pic = db.Column(db.String(100), nullable=False)
