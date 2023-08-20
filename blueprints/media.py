import os

from flask import Blueprint, current_app
bp = Blueprint("media", __name__, url_prefix="/media")


@bp.route("/<path:filename>")
def media_file(filename):
    download_url = current_app.config.get("DOWNLOAD_URL")
    print("downlaodUrl", download_url)
    return os.path.join(download_url, filename)


