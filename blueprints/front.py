import asyncio
import json
import os
import time
from datetime import datetime

import aiohttp
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, g, send_from_directory
from flask_paginate import Pagination
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session
from werkzeug.utils import secure_filename

from exts import db, csrf, cache
from forms.UploadFileForm import UploadFileForm
from forms.post import PublicPostForm
from models.file import ApkInfoModel
from models.post import BoardModel, PostModel, CommentModel
from models.guarantee import GuaranteeModel

from utils import restful

bp = Blueprint("front", __name__, url_prefix="")


async def all_b():
    async with async_session(db.session) as session:
        result = await session.execute(select(BoardModel))
        return result.scalars().all()


@bp.route("/")
async def index():
    # user_id = session['user_id']
    # user = UserModel.query.filter_by(id=user_id).first()
    # print(f"front.index user_id={user_id}, email={user} getargs={request.args['name']}")

    boards = BoardModel.query.all()
    # 获取页码参数
    page = request.args.get("page", type=int, default=1)
    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 当前page的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")

    # 查询对象
    query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)

    # 总共有多少帖子
    total = query_obj.count()
    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)
    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")

    context = {
        "name": ("z11", '22',),
        "cur_time": datetime.now(),
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id,
        "guarantee_url":GuaranteeModel.query.first().gua_pic
    }

    return render_template("front/index.html", **context)


@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()
    return render_template("front/post_detail.html", post=post)


@bp.route("/post/<int:post_id>/comment", methods=['POST'])
# @login_required
def public_comment(post_id):
    print("public_comment", post_id)
    form = PublicPostForm(request.form)
    if form.validate():
        content = form.content.data
        comment = CommentModel(content=content, post_id=post_id, author=g.user)
        db.session.add(comment)
        db.session.commit()
    else:
        for message in form.messages:
            flash(message)
    return redirect(url_for("front.post_detail", post_id=post_id))


@bp.route("/post/public", methods=["GET", "POST"])
def public_post():
    if request.method == "GET":
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)

    else:
        return "nihao"


@bp.post("/upload_file")
@csrf.exempt
def upload_file():
    form = UploadFileForm(request.files)

    file = form.file.data
    current_app.logger.error(f"file {file}")
    if file:
        filename = file.filename
        current_app.logger.info(f"filename {filename}")
        filename = secure_filename(filename)
        current_app.logger.info(f"filename2 {filename}")
        save_path = os.path.join(current_app.config['UPLOAD_URL'], filename)
        file.save(save_path)
        return "save s"

    return f"nihao {form.file.data}"


async def get_ip():
    ip_address = cache.get("ip_address")
    if ip_address:
        return ip_address

    start = time.time()
    url = "http://ip-api.com/json"
    print("start = ", start)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            ip = json.loads(await res.text())['query']
            print("ip = ", ip, "cost time = ", time.time() - start)

            cache.set("ip_address", ip, timeout=100)
            return ip

from concurrent.futures import ProcessPoolExecutor

async def test_get_ip():
    start = time.time()
    print("test_get_ip ", start)
    tasks = []
    for i in range(0, 5):
        tasks.append(get_ip())
    ips = await asyncio.gather(*tasks)
    print("ips ", ips, "cost time ", time.time() - start)
    return ips

@bp.route("/get_apk/<version>")
async def get_apk(version):
    apks = db.session.execute(select(ApkInfoModel).filter_by(version=version)).scalars().all()
    return str(apks[0].join_time) + "11111221"


@bp.route("/update_apk/<string:package_name>")
async def update_apk(package_name):
    apks = db.session.execute(
        select(ApkInfoModel).filter_by(package_name=package_name).order_by(ApkInfoModel.version.desc())).scalars().all()
    data = None
    if apks and len(apks) >= 1:
        apk = apks[0]
        ip = await get_ip()
        filename = secure_filename(apk.name)
        print("filename ", filename)
        data = {
            "version": apk.version,
            "name": apk.name,
            "download_url": f"{ip}{url_for('front.download_file', filename=filename)}",
        }
        return restful.ok(data=data)

    return restful.ok(message="no apk info!", data=data)


@bp.route("/download/<string:filename>")
def download_file(filename):
    file = os.path.join(current_app.config['DOWNLOAD_URL'], filename)
    is_file = os.path.isfile(file)
    current_app.logger.info(f"is_file {is_file}, {file}")
    if is_file:
        return send_from_directory(current_app.config['DOWNLOAD_URL'], filename, as_attachment=True)

    return "不是文件"
