from flask import Blueprint

bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/cms/home")
def cms_home():
    return "cms_home"
