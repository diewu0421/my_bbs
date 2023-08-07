import click

from exts import db
from models.user import PermissionEnum, PermissionModel, RoleModel, UserModel


def my_command():
    click.echo("砸手机asd发")


def create_permission():
    for permission in dir(PermissionEnum):
        if permission.startswith("__"):
            continue
        permissionModel = PermissionModel(name=getattr(PermissionEnum, permission))
        db.session.add(permissionModel)

    db.session.commit()
    click.echo("create-permission success")


def create_role():
    inspector = RoleModel(name="稽查", desc="负责稽查")
    inspector.permissions = PermissionModel.query.filter(
        PermissionModel.name.in_([PermissionEnum.POST, PermissionEnum.COMMENT])).all()

    operator = RoleModel(name="运营", desc="负责网站持续正常运营")
    operator.permissions = PermissionModel.query.filter(PermissionModel.name.in_(
        [PermissionEnum.POST, PermissionEnum.COMMENT, PermissionEnum.FRONT_USER, PermissionEnum.BOARD])).all()

    administrator = RoleModel(name="管理员", desc="负责管理网站的各项事务")
    administrator.permissions = PermissionModel.query.all()

    db.session.add_all([inspector, operator, administrator])
    db.session.commit()
    click.echo("创建角色成功")


def create_test_user():
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    zhangsan = UserModel(name="张三", email="zhagnsan@zlkt.net", password="buzhidao", is_staff=True, role=admin_role)

    operator_role = RoleModel.query.filter_by(name="运营").first()
    lisi = UserModel(name="李四", email="lisi@sina.com", password="buzhidaoLA510", is_staff=True, role=operator_role)

    inspector_role = RoleModel.query.filter_by(name="稽查").first()
    wangwu = UserModel(name="王五", email="wangwu@163.com", password="buzhidaoLA510.", is_staff=True,
                       role=inspector_role)
    db.session.add_all([zhangsan, lisi, wangwu])

    db.session.commit()
    click.echo("创建测试账号成功")


@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--email", "-e")
def create_admin(username, password, email):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    admin = UserModel(name=username, email=email, password=password, role=admin_role, is_staff=True,
                      is_admin=admin_role.name == "管理员")

    db.session.add(admin)
    db.session.commit()
    click.echo(f"创建管理员{admin}成功")


@click.option("--username", "-u")
def del_admin(username):
    admin_role = RoleModel.query.filter_by(name="管理员").first()
    print("admin_role", admin_role)
    del_user = UserModel.query.filter_by(name=username, role=admin_role).first()
    print("del_uer", del_user)
    # db.session.add(del_user)
    db.session.delete(del_user)
    db.session.commit()
    click.echo("del ")
