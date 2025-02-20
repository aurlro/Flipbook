import os
import re
from werkzeug.utils import secure_filename
from flask import current_app
from PyPDF2 import PdfReader
import magic  # pour la détection du type MIME

class FileValidator:
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIME_TYPES = {'application/pdf'}

    @staticmethod
    def is_safe_filename(filename):
        """Vérifie si le nom de fichier est sécurisé"""
        pattern = re.compile(r'^[a-zA-Z0-9_.-]+$')
        return bool(pattern.match(filename))

    @staticmethod
    def check_mime_type(file):
        """Vérifie le type MIME du fichier"""
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)
        return mime in FileValidator.MIME_TYPES

    @staticmethod
    def validate_pdf(file):
        """Validation complète du fichier PDF"""
        if not file or file.filename == '':
            return False, "Aucun fichier fourni"

        if not FileValidator.is_safe_filename(file.filename):
            return False, "Nom de fichier non valide"

        # Vérification de la taille
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > FileValidator.MAX_FILE_SIZE:
            return False, "Fichier trop volumineux"

        # Vérification du type MIME
        if not FileValidator.check_mime_type(file):
            return False, "Type de fichier non autorisé"

        try:
            # Validation du PDF avec PyPDF2
            pdf = PdfReader(file)
            if len(pdf.pages) == 0:
                return False, "PDF invalide ou vide"
            file.seek(0)
            return True, None
        except Exception as e:
            return False, "Fichier PDF invalide"