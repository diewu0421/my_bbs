import random

from flask import Blueprint, render_template, request, current_app, flash, url_for, redirect, session
from flask_mail import Message

from exts import cache, db
from forms.user import RegisterForm, LoginForm
from models.user import UserModel

bp = Blueprint("user", __name__, url_prefix="/user")

BAOBEI_EMAIL = "1241307228@qq.com"


@bp.route("register", methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")

    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            print(f"email = {email}, username = {username}, password={password}, confirm_password={confirm_password}")
            user = UserModel(email=email, password=password, name=username)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("user.register"))


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print("login get")
        return render_template("front/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            print(f"email={email}, password={password}, remember={remember}")
            user = UserModel.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                print('userid', session['user_id'])
                # if remember:
                #     session.permanent = True
                url = url_for("front.index", name="zenglw")
                print(f"url = {url}")
                return redirect(url)

            else:
                flash("邮箱或者密码错误")
                temp = url_for("user.login")
                print("temp = ", temp)
                return redirect(temp)
        else:
            print("form.messags", form.messages)
            for message in form.messages:
                flash(message)

            return render_template("front/login.html")


@bp.route("/mail/captcha")
def mail_captcha():
    email = request.args.get("mail")
    print("email = ", email)
    print("从缓存中获取验证码 ", cache.get(email))

    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ]

    captcha = "".join(random.sample(digits, 4))
    print("发送的验证码为", captcha)
    body = f"【宝贝快睡觉啊】茜茜宝贝的验证码是：{captcha}, 请勿告诉别人！"

    message = Message(subject="验证码",
                      recipients=[email],
                      body=body,
                      )

    # mail.send(message)
    current_app.celery.send_task("send_email", (email, "验证码", body))
    cache.set(email, captcha, timeout=100)

    return "success"
