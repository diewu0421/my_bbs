from celery import Celery
from flask_mail import Message

from exts import mail


def send_message(recipient, subject, body):
    print("send_message was called")

    message = Message(body=body, subject=subject, recipients=[recipient])
    mail.send(message)
    print("发送成功")


def make_celery(app) -> Celery:
    celery = Celery(app.import_name, backend=app.config["CELERY_RESULT_BACKEND"],
                    broker=app.config["CELERY_BROKER_URL"])

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

    celery.task(name="send_email")(send_message)
    return celery


