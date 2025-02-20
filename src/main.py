#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from app.services.config_manager import load_config
from app.services.pdf_processor import process_pdf
from app.services.html_generator import generate_html
# from sharepoint_uploader import upload_to_sharepoint
# from ui import launch_ui

def main():
    # Chargement de la configuration
    config = load_config()
    
    # Exemple de chemin d'un PDF à traiter (peut être paramétré via la configuration ou l'interface)
    pdf_path = config.get('paths', 'pdf_source', fallback="input/sample.pdf")
    destination_path = config.get('paths', 'output_folder', fallback="output")
    
    quality = config.get('settings', 'quality', fallback="medium")
    
    # Traitement du PDF : conversion en images
    print("Traitement du PDF...")
    image_files = process_pdf(pdf_path, destination_path, quality)
    
    # Génération du fichier HTML pour le flipbook
    print("Génération du HTML...")
    flipbook_html = generate_html(image_files, title="Mon Flipbook")
    
    # Sauvegarde du HTML dans le dossier de destination
    html_file = os.path.join(destination_path, "flipbook.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(flipbook_html)
        
    print("Traitement terminé. Vous trouverez le flipbook ici :", html_file)
    
    # Optionnel : lancement de l'interface de configuration
    # launch_ui()

if __name__ == "__main__":
    main()
