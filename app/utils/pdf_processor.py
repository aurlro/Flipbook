"""Module de traitement des fichiers PDF pour le FlipBook."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Processeur de fichiers PDF pour la conversion en images."""

    def __init__(self, config: Dict[str, Union[str, int]]) -> None:
        """
        Initialise le processeur PDF.

        Args:
            config: Dictionnaire de configuration contenant :
                - QUALITY: Qualité de l'image (1-100)
                - OUTPUT_FOLDER: Dossier de sortie pour les images
        """
        self.quality = int(config.get("QUALITY", 75))
        self.output_folder = Path(config.get("OUTPUT_FOLDER", "instance/output"))
        self.dpi = int(self.quality * 1.5)

    def process_pdf(
        self, pdf_path: Union[str, Path]
    ) -> Dict[str, Union[str, int, List[str]]]:
        """
        Traite le PDF et retourne les informations de conversion.

        Args:
            pdf_path: Chemin vers le fichier PDF à traiter

        Returns:
            Dict contenant:
                - status: État de la conversion
                - output_dir: Dossier de sortie des images
                - image_count: Nombre d'images générées
                - images: Liste des chemins des images
        """
        try:
            # Créer un dossier unique pour cette conversion
            pdf_path = Path(pdf_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.output_folder / f"{pdf_path.stem}_{timestamp}"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Conversion du PDF en images
            image_files = self.convert_to_images(pdf_path, output_dir)

            return {
                "status": "success",
                "output_dir": str(output_dir),
                "image_count": len(image_files),
                "images": [str(path) for path in image_files],
            }

        except Exception as e:
            logger.error(f"Erreur lors du traitement du PDF: {str(e)}")
            raise

    def convert_to_images(
        self, pdf_path: Union[str, Path], output_dir: Union[str, Path]
    ) -> List[Path]:
        """
        Convertit chaque page du PDF en image.

        Args:
            pdf_path: Chemin vers le fichier PDF à convertir
            output_dir: Dossier de sortie pour les images

        Returns:
            Liste des chemins des images générées
        """
        image_files = []
        output_dir = Path(output_dir)
        doc = fitz.open(str(pdf_path))

        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(self.dpi / 72, self.dpi / 72))

                image_path = output_dir / f"page_{page_num + 1}.png"
                pix.save(str(image_path))

                image_files.append(image_path)
                logger.info(f"Page {page_num + 1} convertie : {image_path}")

            return image_files

        finally:
            doc.close()
