from flask import session, g, render_template
from models.user import UserModel


def bbs_before_request():
    if "user_id" in session:
        print('useridbbs_before_request', session['user_id'])
        user_id = session.get("user_id")
        try:
            user = UserModel.query.get(user_id)
            setattr(g, "user", user)
        except Exception as e:
            print("22222222222")


def bbs_404_error(error):
    return render_template("errors/404.html"), 404


def bbs_401_error(error):
    return render_template("errors/401.html"), 401


def bbs_500_error(error):
    return render_template("errors/500.html"), 500
