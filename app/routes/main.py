from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from app.utils.validators import FileValidator
from app.utils.pdf_processor import PDFProcessor

import os
<<<<<<< HEAD
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
=======
import logging

main_bp = Blueprint('main', __name__)

# Configuration du logging
logging.basicConfig(
    filename='flipbook.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/config')
>>>>>>> ba066e810d1d85ad7cf37c29561aa5b4baee6d02
def config_page():
    config = {
<<<<<<< HEAD
        "pdf_source": current_app.config.get("PDF_SOURCE", ""),
        "output_folder": current_app.config.get("OUTPUT_FOLDER", ""),
        "quality": current_app.config.get("QUALITY", 100),
=======
        'quality': current_app.config['QUALITY'],
        'pdf_source': current_app.config['PDF_SOURCE'],
        'output_folder': current_app.config['OUTPUT_FOLDER']
>>>>>>> ba066e810d1d85ad7cf37c29561aa5b4baee6d02
    }
    return render_template("config.html", config=config)

<<<<<<< HEAD

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
=======
@main_bp.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        file = request.files['pdf_file']
        validator = FileValidator()
        is_valid, error_message = validator.validate_pdf(file)
        
        if not is_valid:
            flash(error_message, 'error')
            return redirect(request.url)
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['PDF_SOURCE'], filename)
            file.save(filepath)
            
            logger.info(f"Fichier PDF '{filename}' téléchargé avec succès")
            flash('Fichier PDF téléchargé avec succès', 'success')
            return redirect(url_for('main.process_pdf', filename=filename))
        
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement du fichier: {str(e)}")
            flash(f"Erreur lors du téléchargement: {str(e)}", 'error')
            return redirect(request.url)
    
    return render_template('convert.html')

@main_bp.route('/history')
def history_page():
    # Récupération de l'historique des conversions
    history = []  # À implémenter : récupération depuis une base de données ou des fichiers
    return render_template('history.html', history=history)

@main_bp.route('/logs')
def logs_page():
    # Lecture du fichier de log
    try:
        with open('flipbook.log', 'r') as f:
            logs = f.readlines()[-150:]  # Dernières 150 lignes
    except FileNotFoundError:
        logs = []
    return render_template('logs.html', logs=logs)

@main_bp.route('/process/<filename>')
def process_pdf(filename):
    try:
        filepath = os.path.join(current_app.config['PDF_SOURCE'], filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas")

        # Création du processeur PDF avec la configuration actuelle
        processor = PDFProcessor(current_app.config)
        
        # Traitement du PDF
        result = processor.process_pdf(filepath)
        
        # Mise à jour des logs
        logger.info(f"PDF '{filename}' traité avec succès: {result['image_count']} pages converties")
        
        return jsonify({
            'status': 'success',
            'message': f"PDF converti avec succès en {result['image_count']} images",
            'output_dir': result['output_dir'],
            'images': result['images']
        })

    except Exception as e:
        error_msg = f"Erreur lors du traitement du PDF: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
>>>>>>> ba066e810d1d85ad7cf37c29561aa5b4baee6d02
