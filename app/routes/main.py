"""Routes principales de l'application Flask."""

import logging
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.utils import secure_filename

from app.utils.pdf_processor import PDFProcessor
from app.utils.validators import FileValidator

# Création du Blueprint
main_bp = Blueprint("main", __name__)

# Configuration du logging
logging.basicConfig(
    filename="flipbook.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@main_bp.route("/")
def index():
    """Page d'accueil de l'application."""
    return render_template("index.html")


@main_bp.route("/upload", methods=["GET", "POST"])
def upload():
    """Gestion du téléchargement des PDF."""
    if request.method == "POST":
        if "pdf_file" not in request.files:
            flash("Aucun fichier sélectionné", "error")
            return redirect(request.url)

        file = request.files["pdf_file"]
        validator = FileValidator()
        is_valid, error_message = validator.validate_pdf(file)

        if not is_valid:
            flash(error_message, "error")
            return redirect(request.url)

        try:
            filename = secure_filename(file.filename)
            filepath = Path(current_app.config["UPLOAD_FOLDER"]) / filename
            file.save(filepath)

            processor = PDFProcessor(current_app.config)
            result = processor.process_pdf(filepath)

            flash("PDF converti avec succès", "success")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Erreur lors du traitement: {str(e)}")
            flash(f"Erreur: {str(e)}", "error")
            return jsonify({"error": str(e)}), 500

    return render_template("upload.html")


@main_bp.route("/preview/<path:filename>")
def preview_image(filename):
    """Affiche une image convertie."""
    return send_from_directory(current_app.config["OUTPUT_FOLDER"], filename)


@main_bp.route("/config")
def config_page():
    """Page de configuration."""
    config = {
        "quality": current_app.config["QUALITY"],
        "pdf_source": current_app.config["PDF_SOURCE"],
        "output_folder": current_app.config["OUTPUT_FOLDER"],
    }
    return render_template("config.html", config=config)


@main_bp.route("/convert")
def convert():
    """Page de conversion."""
    return render_template("convert.html")


@main_bp.route("/history")
def history_page():
    """Page d'historique des conversions."""
    # Logique pour récupérer l'historique des conversions
    return render_template("history.html")
