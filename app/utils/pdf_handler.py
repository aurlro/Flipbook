"""
Module de traitement des fichiers PDF pour Flipbook.
Gère la conversion des PDF en images et leur préparation pour le flipbook.
"""

import logging
from pathlib import Path
from typing import List, Tuple

import fitz  # PyMuPDF
from flask import current_app
from PIL import Image

# Configuration du logging
logger = logging.getLogger(__name__)


class PDFHandler:
    """Gestionnaire de traitement des fichiers PDF."""

    ALLOWED_EXTENSIONS = {"pdf"}
    IMAGE_FORMAT = "PNG"
    DPI = 300
    QUALITY = 95

    @classmethod
    def allowed_file(cls, filename: str) -> bool:
        """
        Vérifie si l'extension du fichier est autorisée.

        Args:
            filename (str): Nom du fichier à vérifier

        Returns:
            bool: True si l'extension est autorisée, False sinon
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in cls.ALLOWED_EXTENSIONS
        )

    @classmethod
    def create_output_directory(cls, pdf_path: str) -> Path:
        """
        Crée le répertoire de sortie pour les images.

        Args:
            pdf_path (str): Chemin du fichier PDF

        Returns:
            Path: Chemin du répertoire de sortie
        """
        output_dir = Path(current_app.config["OUTPUT_FOLDER"]) / Path(pdf_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    @classmethod
    def optimize_image(cls, image: Image.Image, quality: int = QUALITY) -> Image.Image:
        """
        Optimise une image pour le web.

        Args:
            image (Image.Image): Image à optimiser
            quality (int): Qualité de compression (1-100)

        Returns:
            Image.Image: Image optimisée
        """
        # Conversion en RGB si nécessaire
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        # Redimensionnement si trop grande
        max_size = current_app.config.get("MAX_IMAGE_SIZE", 2000)
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        return image

    @classmethod
    def process_pdf_file(cls, pdf_path: str) -> Tuple[str, List[str]]:
        """
        Convertit un PDF en images et prépare le flipbook.

        Args:
            pdf_path (str): Chemin du fichier PDF

        Returns:
            Tuple[str, List[str]]: (Chemin sortie, Liste chemins images)

        Raises:
            Exception: En cas d'erreur lors du traitement
        """
        try:
            output_dir = cls.create_output_directory(pdf_path)
            image_files = []

            logger.info(f"Traitement du PDF: {pdf_path}")

            # Ouverture du PDF avec PyMuPDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            for page_num in range(total_pages):
                # Conversion de la page en image
                page = doc[page_num]
                matrix = fitz.Matrix(cls.DPI / 72, cls.DPI / 72)
                pix = page.get_pixmap(matrix=matrix)

                # Création de l'image PIL
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Optimisation de l'image
                img = cls.optimize_image(img)

                # Sauvegarde de l'image
                image_filename = f"page_{page_num + 1}.{cls.IMAGE_FORMAT.lower()}"
                image_path = output_dir / image_filename
                img.save(
                    image_path,
                    format=cls.IMAGE_FORMAT,
                    optimize=True,
                    quality=cls.QUALITY,
                )

                image_files.append(image_filename)
                msg = f"Page {page_num + 1}/{total_pages} convertie: {image_filename}"
                logger.debug(msg)

            doc.close()
            logger.info(f"Conversion terminée: {len(image_files)} pages traitées")

            return str(output_dir), image_files

        except Exception as e:
            error_msg = f"Erreur lors du traitement du PDF: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @classmethod
    def cleanup_old_files(cls, max_age_hours: int = 24) -> None:
        """
        Nettoie les anciens fichiers de sortie.

        Args:
            max_age_hours (int): Âge maximum des fichiers en heures
        """
        try:
            output_folder = Path(current_app.config["OUTPUT_FOLDER"])
            current_time = Path.ctime(output_folder)

            for item in output_folder.glob("*"):
                if item.is_dir():
                    age_seconds = (current_time - Path.ctime(item)).total_seconds()
                    # Suppression si le dossier est trop vieux
                    if age_seconds > max_age_hours * 3600:
                        for file in item.glob("*"):
                            file.unlink()
                        item.rmdir()
                        logger.info(f"Dossier nettoyé: {item}")

        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {str(e)}")
