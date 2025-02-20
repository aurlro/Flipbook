from werkzeug.utils import secure_filename
from flask import current_app
from PyPDF2 import PdfReader
import os

class FileValidator:
    @staticmethod
    def allowed_file(filename):
        """Vérifie si l'extension du fichier est autorisée"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'pdf'}

    @staticmethod
    def validate_pdf(file):
        """Valide un fichier PDF"""
        if not file:
            return False, "Aucun fichier fourni"

        if file.filename == '':
            return False, "Aucun fichier sélectionné"

        if not FileValidator.allowed_file(file.filename):
            return False, "Type de fichier non autorisé. Seuls les PDF sont acceptés."

        try:
            # Test de lecture du PDF
            file.seek(0)
            PdfReader(file)
            file.seek(0)  # Réinitialise le curseur
            return True, None
        except Exception as e:
            return False, f"Le fichier n'est pas un PDF valide : {str(e)}"