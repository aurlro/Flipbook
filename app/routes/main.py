from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from app.utils.validators import FileValidator
from app.utils.pdf_processor import PDFProcessor

import os
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
def config_page():
    config = {
        'quality': current_app.config['QUALITY'],
        'pdf_source': current_app.config['PDF_SOURCE'],
        'output_folder': current_app.config['OUTPUT_FOLDER']
    }
    return render_template('config.html', config=config)

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