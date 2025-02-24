from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = "votre-clé-secrète"


class UploadForm(FlaskForm):
    pdf_file = FileField("PDF File", validators=[FileRequired()])
    submit = SubmitField("Upload")


@app.route("/")
def index():
    return "Test OK"


if __name__ == "__main__":
    app.run(debug=True)
