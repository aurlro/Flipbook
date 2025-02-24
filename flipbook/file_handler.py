import os
import uuid
from datetime import datetime
from pathlib import Path

from werkzeug.utils import secure_filename

from .pdf_handler import PDFHandler


class FileHandler:
    def __init__(self, app):
        self.app = app
        self.pdf_handler = PDFHandler(app.config["PDF_FOLDER"])
        self.upload_folder = app.config["UPLOAD_FOLDER"]
        self.allowed_extensions = app.config["ALLOWED_EXTENSIONS"]

    def allowed_file(self, filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions
        )

    def save_file(self, file):
        """Sauvegarde un fichier et retourne les informations nécessaires."""
        if not file or not self.allowed_file(file.filename):
            return {"success": False, "error": "Type de fichier non autorisé"}

        try:
            # Générer un nom de fichier unique
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{extension}"

            # Chemin de sauvegarde
            save_path = Path(self.upload_folder) / unique_filename
            file.save(str(save_path))

            # Si c'est un PDF, le convertir
            if extension == "pdf":
                result = self.pdf_handler.convert_pdf_to_images(save_path)
                # Supprimer le PDF original après conversion
                save_path.unlink()

                if result["success"]:
                    return {
                        "success": True,
                        "type": "pdf",
                        "pages": [str(p) for p in result["image_paths"]],
                        "num_pages": result["num_pages"],
                        "original_filename": original_filename,
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erreur de conversion PDF: {result['error']}",
                    }
            else:
                # Pour les images normales
                return {
                    "success": True,
                    "type": "image",
                    "path": str(save_path),
                    "original_filename": original_filename,
                }

        except Exception as e:
            return {"success": False, "error": f"Erreur lors du traitement: {str(e)}"}
