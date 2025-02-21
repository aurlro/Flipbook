import os
from app.utils.pdf_processor import process_pdf
from app.utils.html_generator import generate_html

from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
)
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join
from app.utils.validators import FileValidator
from app.utils.pdf_processor import PDFProcessor
import os
import logging
from functools import wrap

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # Exemple de chargement des pages
    output_folder = current_app.config["OUTPUT_FOLDER"]
    pages = []

    # Récupérer les chemins des images dans l'ordre
    for file in sorted(os.listdir(output_folder)):
        if file.endswith((".jpg", ".png", ".jpeg")):
            page_path = f"/output/{file}"  # Chemin relatif pour l'URL
            pages.append(page_path)

    return render_template("flipbook_template.html", pages=pages)


@main.route("/config")
def config_page():
    # Récupérer les configurations actuelles
    config = {
        "pdf_source": current_app.config.get("PDF_SOURCE", ""),
        "output_folder": current_app.config.get("OUTPUT_FOLDER", ""),
        "quality": current_app.config.get("QUALITY", 100),
    }
    return render_template("config.html", config=config)


@main.route("/convert")
def convert():
    return render_template("convert.html")


@main.route("/history")
def history_page():
    # Vous pourriez ajouter ici la logique pour récupérer l'historique des conversions
    conversions = []  # À remplacer par la vraie récupération des données
    return render_template("history.html", conversions=conversions)


@main.route("/logs")
def logs_page():
    # Vous pourriez ajouter ici la logique pour récupérer les logs
    logs = []  # À remplacer par la vraie récupération des logs
    return render_template("logs.html", logs=logs)


@main.route("/process-pdf", methods=["POST"])
def process_pdf_route():
    try:
        pdf_path = current_app.config["PDF_SOURCE"]
        output_folder = current_app.config["OUTPUT_FOLDER"]
        quality = current_app.config["QUALITY"]

        image_files = process_pdf(pdf_path, output_folder, quality)
        flipbook_html = generate_html(image_files)

        # Vous pourriez ajouter ici l'enregistrement dans l'historique

        flash("PDF traité avec succès", "success")
        return jsonify(
            {
                "status": "success",
                "message": "PDF processed successfully",
                "files": image_files,
            }
        )
    except Exception as e:
        flash(f"Erreur lors du traitement du PDF: {str(e)}", "error")
        return jsonify({"status": "error", "message": str(e)}), 500


@main.route("/update-config", methods=["POST"])
def update_config():
    try:
        # Mettre à jour la configuration
        current_app.config["PDF_SOURCE"] = request.form.get("pdf_source")
        current_app.config["OUTPUT_FOLDER"] = request.form.get("output_folder")
        current_app.config["QUALITY"] = int(request.form.get("quality", 100))

        flash("Configuration mise à jour avec succès", "success")
        return jsonify({"status": "success"})
    except Exception as e:
        flash(f"Erreur lors de la mise à jour de la configuration: {str(e)}", "error")
        return jsonify({"status": "error", "message": str(e)}), 500
