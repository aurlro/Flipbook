from flask import Blueprint, render_template, current_app, request
from app.utils.pdf_processor import process_pdf
from app.utils.html_generator import generate_html

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Route principale affichant la page d'accueil"""
    return render_template("index.html")


@bp.route("/process-pdf", methods=["POST"])
def process_pdf_route():
    """Route pour traiter le PDF et générer le flipbook"""
    try:
        pdf_path = current_app.config["PDF_SOURCE"]
        output_folder = current_app.config["OUTPUT_FOLDER"]
        quality = current_app.config["QUALITY"]

        # Traitement du PDF et génération des images
        image_files = process_pdf(pdf_path, output_folder, quality)

        # Génération du HTML pour le flipbook
        flipbook_html = generate_html(image_files)

        return {
            "status": "success",
            "message": "PDF processed successfully",
            "html": flipbook_html,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@bp.errorhandler(404)
def not_found_error(error):
    """Gestionnaire pour les erreurs 404"""
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    """Gestionnaire pour les erreurs 500"""
    return render_template("500.html"), 500
