from flask import Blueprint,render_template

bp = Blueprint("front", __name__, url_prefix="/front")


@bp.route("/index")
def index():
    print("asdfasdf")
    return render_template("front/index.html")





