from pathlib import Path
from config.config import config

def init_directories(app_config):
    """Initialise les dossiers nécessaires"""
    directories = [
        app_config.PDF_SOURCE,
        app_config.OUTPUT_FOLDER,
        app_config.TEMP_FOLDER,
        app_config.LOGS_DIR
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, mode=0o750, exist_ok=True)