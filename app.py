from flask import Flask
from flask_migrate import Migrate
from gevent import pywsgi
from flask_wtf import CSRFProtect

import commands
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from config import DevelopmentConfig
from exts import db, mail, cache
from bbs_celery import make_celery

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.cli.command("my-command")(commands.my_command)
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create_role")(commands.create_role)
app.cli.command("create_test_user")(commands.create_test_user)
app.cli.command("create_admin")(commands.create_admin)
app.cli.command("del_admin")(commands.del_admin)

migrate = Migrate(app, db)


@app.route("/")
def hello() -> str:
    return "hello world"


db.init_app(app)
mail.init_app(app)
cache.init_app(app)

print('register ', user_bp)
app.register_blueprint(user_bp)
app.register_blueprint(front_bp)
app.register_blueprint(cms_bp)

# @app.route("/register")
# def register():
#     print("register")
#     return render_template("front/register.html")
CSRFProtect(app)

celery = make_celery(app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    # server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    # server.serve_forever()
