"""Module de validation des fichiers."""

import os

import fitz


class FileValidator:
    """Classe de validation des fichiers."""

    ALLOWED_EXTENSIONS = {"pdf"}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

    @classmethod
    def allowed_file(cls, filename):
        """Vérifie si l'extension du fichier est autorisée."""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in cls.ALLOWED_EXTENSIONS
        )

    @classmethod
    def validate_pdf(cls, file):
        """Valide un fichier PDF."""
        if not file:
            return False, "Aucun fichier fourni"

        if file.filename == "":
            return False, "Aucun fichier sélectionné"

        if not cls.allowed_file(file.filename):
            return False, "Type de fichier non autorisé. Seuls les PDF sont acceptés."

        # Vérification de la taille
        file.seek(0, os.SEEK_END)
        size = file.tell()
        if size > cls.MAX_FILE_SIZE:
            max_size_mb = cls.MAX_FILE_SIZE / 1024 / 1024
            return (False, f"Le fichier est trop volumineux (max {max_size_mb:.1f}MB)")

        try:
            # Test de lecture du PDF avec PyMuPDF
            file.seek(0)
            doc = fitz.open(stream=file.read(), filetype="pdf")
            page_count = len(doc)
            doc.close()

            if page_count == 0:
                return False, "Le PDF ne contient aucune page"

            file.seek(0)
            return True, None

        except Exception as e:
            return False, f"Le fichier n'est pas un PDF valide : {str(e)}"
