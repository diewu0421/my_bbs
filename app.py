import logging

from flask import Flask,g
from flask_migrate import Migrate
from gevent import pywsgi
from flask_wtf import CSRFProtect
from flask_socketio import SocketIO

from gevent import pywsgi

import commands
from bbs_celery import make_celery
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from config import DevelopmentConfig
from exts import db, mail, cache,csrf
# from bbs_celery import make_celery
import models.post
import hooks

from utils.common import get_html

from tasks.my_tasks import hh

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("build.log", encoding="utf-8")
app.logger.info("123412341111111111111")
app.logger.addHandler(file_handler)
with app.app_context():
    app.before_request(hooks.bbs_before_request)

    app.cli.command("my-command")(commands.my_command)
    app.cli.command("create-permission")(commands.create_permission)
    app.cli.command("create_role")(commands.create_role)
    app.cli.command("create_test_user")(commands.create_test_user)
    app.cli.command("create_admin")(commands.create_admin)
    app.cli.command("del_admin")(commands.del_admin)
    app.cli.command("create_board")(commands.create_board)
    app.cli.command("create-test-post")(commands.create_test_post)

    migrate = Migrate(app, db)

    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    print('register ', user_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(cms_bp)
    celery= make_celery(app)
    from flask import current_app

    app.jinja_env.is_async = True
    app.jinja_env.globals['get_html'] = get_html
    app.errorhandler(404)(hooks.bbs_404_error)


    csrf.init_app(app)

    print("app id ",id(app), id(current_app), "celery", current_app.celery, "   111 ", app.celery )

@app.template_filter('custom_filter')
def custom_filter(str):
    return str +"_____"
# @app.route("/register")
# def register():
#     print("register")
#     return render_template("front/register.html")


@app.route("/test_celery", methods=["GET"])
def test_celery():
    print("task _celery")
    hh_task = hh.delay()
    print(hh_task)
    return "test_celery"


from models.file import ApkInfoModel
# celery = make_celery(app)
if __name__ == '__main__':
    app.run( debug=False,host="0.0.0.0", port=80)
    # socketio.run(app, host = "0.0.0.0", port=80, debug=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    # server.serve_forever()

    # server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    # server.serve_forever()