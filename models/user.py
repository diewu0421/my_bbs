from datetime import datetime
from enum import Enum

from shortuuid import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


class PermissionEnum(Enum):
    BOARD = "板块"
    POST = "帖子"
    COMMENT = "评论"
    FRONT_USER = "前台用户"
    CMS_USER = "后台用户"


class PermissionModel(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)


role_permission_table = db.Table(
    "role_permission_table",
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class RoleModel(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    permissions = db.relationship("PermissionModel", secondary=role_permission_table, backref="roles")


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True, default=uuid)
    name = db.Column(db.String(100), nullable=False, )
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    avatar = db.Column(db.String(200), nullable=True)
    signature = db.Column(db.String(300))
    is_staff = db.Column(db.Boolean, nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("RoleModel", backref="users")

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs["password"]
            kwargs.pop('password')
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return self.name + "  " + self._password

    def __str__(self):
        return f"name:{self.name}, password:{self.password}"

    def has_permission(self, permission):
        return permission in [permission.name for permission in self.role.permissions]
    # def __str__(self):

    #     return "name=$us"

# if __name__ == '__main__':
#     user = UserModel(name="曾令文", password="buzhidao")
#
#     print(user.check_password("buzhidao"))
#     print(user)

#     print(dir(PermissionEnum))
#     print(getattr(PermissionEnum, "COMMENT"))
#     print(PermissionEnum.BOARD)
