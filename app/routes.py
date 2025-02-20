from flask import Flask, render_template, current_app, request

# Initialisation de l'application Flask
main = Flask(__name__)

@main.route('/')
def index():
    """Route principale affichant la page d'accueil"""
    return render_template('index.html')

@main.route('/process-pdf', methods=['POST'])
def process_pdf_route():
    """Route pour traiter le PDF et générer le flipbook"""
    try:
        pdf_path = current_app.config['PDF_SOURCE']
        output_folder = current_app.config['OUTPUT_FOLDER']
        quality = current_app.config['QUALITY']

        from app.services.pdf_processor import process_pdf
        from app.services.html_generator import generate_html

        image_files = process_pdf(pdf_path, output_folder, quality)
        flipbook_html = generate_html(image_files)

        return {
            'status': 'success',
            'message': 'PDF processed successfully',
            'html': flipbook_html
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 500

@main.errorhandler(404)
def not_found_error(error):
    """Gestionnaire pour les erreurs 404"""
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    """Gestionnaire pour les erreurs 500"""
    return render_template('500.html'), 500