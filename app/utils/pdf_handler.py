import os
from PIL import Image
import PyPDF2
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_pdf_file(pdf_path):
    """
    Convertit un PDF en images et prépare le flipbook
    """
    output_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], 
                             os.path.splitext(os.path.basename(pdf_path))[0])
    os.makedirs(output_dir, exist_ok=True)

    try:
        pdf = PyPDF2.PdfReader(pdf_path)
        # Conversion et traitement à implémenter selon vos besoins
        return output_dir
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du PDF: {str(e)}")