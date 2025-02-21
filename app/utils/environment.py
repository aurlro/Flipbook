import os
from pathlib import Path


def verify_environment(app):
    """Vérifie et crée les dossiers nécessaires"""
    required_folders = [
        app.config["PDF_SOURCE"],
        app.config["OUTPUT_FOLDER"],
        app.config["TEMP_FOLDER"],
        app.config["LOGS_DIR"],
    ]

    for folder in required_folders:
        Path(folder).mkdir(parents=True, mode=0o750, exist_ok=True)

    # Vérification des permissions
    for folder in required_folders:
        if not os.access(folder, os.W_OK):
            app.logger.error(f"Le dossier {folder} n'est pas accessible en écriture")
            return False

    return True
