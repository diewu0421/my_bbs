import random

from flask import Blueprint, render_template, request, current_app
from flask_mail import Message

from exts import mail, cache

bp = Blueprint("user", __name__, url_prefix="/user")

BAOBEI_EMAIL = "1241307228@qq.com"

@bp.route("register", methods=["POST", "GET"])
def register():
    print("start register")

    return render_template("front/register.html")


@bp.route("/mail/captcha")
def mail_captcha():
    email = request.args.get("mail")
    email = "1241307228@qq.com"
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
