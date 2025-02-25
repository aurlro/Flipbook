import os
import tempfile
from pathlib import Path

from pdf2image import convert_from_path

# Essayer d'importer PdfReader de différentes sources
try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        from PyPDF2 import PdfFileReader as PdfReader


class PDFHandler:
    def __init__(self, upload_folder):
        self.upload_folder = Path(upload_folder)
        self.temp_dir = Path(tempfile.gettempdir()) / "flipbook_pdf"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def convert_pdf_to_images(self, pdf_path):
        """Convertit un PDF en images."""
        try:
            # Vérifier si c'est un PDF valide
            with open(pdf_path, "rb") as pdf_file:
                pdf = PdfReader(pdf_file)
                num_pages = len(pdf.pages)

            # Convertir les pages en images
            images = convert_from_path(
                pdf_path,
                dpi=200,  # Résolution des images
                fmt="jpg",
                output_folder=str(self.temp_dir),
                paths_only=True,
            )

            # Déplacer les images vers le dossier static
            image_paths = []
            for i, temp_path in enumerate(images):
                temp_path = Path(temp_path)
                new_filename = f"pdf_page_{Path(pdf_path).stem}_{i+1}.jpg"
                dest_path = self.upload_folder / new_filename

                # Déplacer l'image
                if dest_path.exists():
                    dest_path.unlink()  # Supprimer si existe déjà
                temp_path.rename(dest_path)
                image_paths.append(dest_path)

            return {
                "success": True,
                "num_pages": num_pages,
                "image_paths": image_paths,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def cleanup(self):
        """Nettoie les fichiers temporaires."""
        try:
            for file in self.temp_dir.glob("*"):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file}: {e}")
        except Exception as e:
            print(f"Erreur lors du nettoyage: {e}")
