from flask_mail import Message

from exts import mail
from tasks import celery_app
from flask import current_app


@celery_app.task
def hh():
    print("111111111 2222")


@celery_app.task
def send_message(recipient, subject, body):
    print("send_message was called ", id(current_app))
    message = Message(body=body, subject=subject, recipients=[recipient])
    mail.send(message)
    print("发送成功")
