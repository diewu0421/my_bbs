from flask_caching import Cache
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

mail = Mail()

cache = Cache()
