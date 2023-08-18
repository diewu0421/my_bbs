from flask_wtf.file import FileAllowed
from wtforms import FileField

from forms.baseforms import BaseForm


class UploadFileForm(BaseForm):
    file = FileField(validators=[FileAllowed(['jpg', 'png','mp4', 'webp', 'mp3', 'jpeg'])])

