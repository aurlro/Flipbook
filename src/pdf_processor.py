import os
import fitz  # PyMuPDF

def process_pdf(pdf_path: str, output_folder: str, quality: str = "medium"):
    """
    Convertit un PDF en une série d'images.
    La qualité peut être "low", "medium" ou "high", qui influencera le facteur de zoom.
    Retourne la liste des chemins vers les images générées.
    """
    
    quality_zoom = {
        "low": 1.0,
        "medium": 2.0,
        "high": 3.0
    }
    
    zoom = quality_zoom.get(quality, 2.0)
    
    # Création du dossier de sortie
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(output_folder, pdf_name)
    os.makedirs(output_dir, exist_ok=True)
    
    image_paths = []
    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            image_filename = f"page_{page_num+1:03d}.jpg"
            image_path = os.path.join(output_dir, image_filename)
            pix.save(image_path)
            image_paths.append(image_path)
    return image_paths
