import logging

from flask import Blueprint, request, render_template, current_app, g, redirect, url_for, flash
from werkzeug.datastructures import CombinedMultiDict

from forms.guarantee import GuaranteeForm
from utils import restful

bp = Blueprint("guarantee", __name__ , url_prefix="/guarantee")
@bp.route("/enter", methods=["GET", "POST"])
def enter():
    if request.method == "GET":
        # print("gua ", request.args.get("gua_number", type=str, default=""))
        print("gua", request.args.get("gua_number"))
        context = {
            "need_right": False,
            **request.args.to_dict()
        }
        return render_template("guarantee/enter.html", **context)
    else:
        form = GuaranteeForm(CombinedMultiDict([request.form, request.files]))
        gua_number = form.gua_number.data
        amount = form.amount.data
        warrantee = form.warrantee.data
        beneficiary = form.beneficiary.data
        query_code = form.query_code.data
        gua_pic = form.gua_pic.data
        if form.validate():
            return restful.ok(message="录入成功")
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for("guarantee.enter", gua_number=gua_number, amount =amount, warrantee =warrantee, beneficiary = beneficiary, query_code=query_code, gua_pic=gua_pic))

