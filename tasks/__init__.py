from celery import Celery
from config import DevelopmentConfig


def make_celery():
    celery = Celery("default", backend=DevelopmentConfig.CELERY_BROKER_URL,
                    broker=DevelopmentConfig.CELERY_RESULT_BACKEND ,
                    include=['tasks.my_tasks'])

# celery.task(name="send_mail")(send_mail)
    return celery


celery_app = make_celery()

print("create_celerY", celery_app)