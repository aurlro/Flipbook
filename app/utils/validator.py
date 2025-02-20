import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from flask import current_app

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class FileValidator:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_pdf(file):
        errors = []
        
        # Vérification de l'extension
        if not FileValidator.allowed_file(file.filename):
            errors.append('Format de fichier non autorisé. Seuls les PDF sont acceptés.')
            return errors
        
        # Vérification de la taille
        if len(file.read()) > MAX_FILE_SIZE:
            errors.append('Le fichier est trop volumineux (max 10MB)')
            file.seek(0)  # Réinitialiser le curseur du fichier
            return errors
            
        # Validation du PDF
        try:
            file.seek(0)  # Réinitialiser le curseur du fichier
            PdfReader(file)
        except Exception as e:
            errors.append('Le fichier PDF semble être corrompu ou invalide')
            return errors
            
        file.seek(0)  # Réinitialiser le curseur pour utilisation ultérieure
        return errors

    @staticmethod
    def save_file(file):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath