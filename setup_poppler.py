import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path


def setup_poppler_windows():
    """Configure Poppler pour Windows."""
    POPPLER_URL = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.11.0-0/Release-23.11.0-0.zip"
    POPPLER_DIR = "C:\\Poppler"

    print("Configuration de Poppler pour Windows...")

    try:
        # Créer le dossier Poppler s'il n'existe pas
        Path(POPPLER_DIR).mkdir(parents=True, exist_ok=True)

        # Télécharger Poppler
        print("Téléchargement de Poppler...")
        zip_path = Path(POPPLER_DIR) / "poppler.zip"
        urllib.request.urlretrieve(POPPLER_URL, zip_path)

        # Extraire le zip
        print("Extraction des fichiers...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(POPPLER_DIR)

        # Nettoyer
        zip_path.unlink()

        # Ajouter au PATH
        bin_path = str(Path(POPPLER_DIR) / "Library" / "bin")
        if bin_path not in os.environ["PATH"]:
            print("Ajout de Poppler au PATH...")
            os.system(f'setx PATH "%PATH%;{bin_path}"')

        print("Installation de Poppler terminée!")
        print(f"Poppler installé dans: {POPPLER_DIR}")
        print(
            "Veuillez redémarrer votre terminal pour que les changements prennent effet."
        )

    except Exception as e:
        print(f"Erreur lors de l'installation: {e}")


if __name__ == "__main__":
    if sys.platform == "win32":
        setup_poppler_windows()
    else:
        print("Ce script est uniquement pour Windows.")
