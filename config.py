from datetime import timedelta


class BaseConfig(object):
    SECRET_KEY = "yoasdfkj"
    PER_PAGE_COUNT=10
    SQLALCHEMY_TRACK_MODIFICATION = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)


class DevelopmentConfig(BaseConfig):
    HOSTNAME = "127.0.0.1"
    PORT = 3306
    USER_NAME = "root"
    PASSWORD = "buzhidao"
    DATABASE = "pythonbbs"
    DATA_STR = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
    SQLALCHEMY_DATABASE_URI = DATA_STR

    DOWNLOAD_URL  = "static"
    UPLOAD_URL  = "static/upload/"

    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "317335825@qq.com"
    MAIL_PASSWORD = "avefthfkkphacbcc"
    MAIL_DEFAULT_SENDER = "317335825@qq.com"

    # REDIS_URL = "redis://:buzhidao@localhost/0"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_PASSWORD = "buzhidao"

    CELERY_BROKER_URL = "redis://:buzhidao@127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://:buzhidao@127.0.0.1:6379/0"
