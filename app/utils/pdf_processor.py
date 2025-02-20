import os
import fitz  # PyMuPDF
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, config):
        self.quality = config.get('QUALITY', 75)
        self.output_folder = config.get('OUTPUT_FOLDER')
        self.dpi = int(self.quality * 1.5)

    def process_pdf(self, pdf_path):
        """
        Traite le PDF et retourne les informations de conversion
        """
        try:
            # Créer un dossier unique pour cette conversion
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.basename(pdf_path)
            output_dir = os.path.join(
                self.output_folder,
                f"{os.path.splitext(filename)[0]}_{timestamp}"
            )
            os.makedirs(output_dir, exist_ok=True)

            # Conversion du PDF en images
            image_files = self.convert_to_images(pdf_path, output_dir)

            return {
                'status': 'success',
                'output_dir': output_dir,
                'image_count': len(image_files),
                'images': image_files
            }

        except Exception as e:
            logger.error(f"Erreur lors du traitement du PDF: {str(e)}")
            raise

    def convert_to_images(self, pdf_path, output_dir):
        """
        Convertit chaque page du PDF en image
        """
        image_files = []
        doc = fitz.open(pdf_path)

        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(self.dpi/72, self.dpi/72))
                
                image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
                pix.save(image_path)
                
                image_files.append(image_path)
                logger.info(f"Page {page_num + 1} convertie : {image_path}")

            return image_files

        finally:
            doc.close()