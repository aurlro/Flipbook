from pdf2image import convert_from_path
import os

def process_pdf(pdf_path: str, output_folder: str, quality: str = "medium"):
    """
    Convertit un PDF en une série d'images en utilisant pdf2image.
    La qualité peut être "low", "medium" ou "high", qui influencera le DPI.
    Retourne la liste des chemins vers les images générées.
    """
    # Chemin vers poppler
    POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"
    
    # Mapping de la qualité vers des valeurs DPI
    quality_dpi = {
        "low": 100,
        "medium": 200,
        "high": 300
    }
    
    # Mapping de la qualité vers la compression JPEG
    quality_jpeg = {
        "low": 60,
        "medium": 80,
        "high": 95
    }
    
    dpi = quality_dpi.get(quality, 200)
    jpeg_quality = quality_jpeg.get(quality, 80)
    
    # Création du dossier de sortie avec le nom du PDF
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(output_folder, pdf_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Convertir les pages en images en spécifiant le chemin vers poppler
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=POPPLER_PATH  # Ajout du chemin vers poppler ici
    )
    
    # Sauvegarder chaque page comme une image 
    image_files = []
    for i, image in enumerate(images):
        image_filename = f"page_{i+1:03d}.jpg"
        image_path = os.path.join(output_dir, image_filename)
        image.save(image_path, 'JPEG', quality=jpeg_quality)
        image_files.append(image_path)
    
    return image_files
