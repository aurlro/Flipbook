from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class UploadForm(FlaskForm):
    pdf_file = FileField("Sélectionner un PDF", validators=[FileRequired()])
    submit = SubmitField("Envoyer")
