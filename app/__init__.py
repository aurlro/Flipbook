"""Module d'initialisation de l'application Flask."""

import os
from flask import Flask
from pathlib import Path

def create_app(config_class=None):
    """
    Crée et configure l'application Flask.
    
    Args:
        config_class: Classe de configuration à utiliser

    Returns:
        L'application Flask configurée
    """
    app = Flask(__name__)

    # Configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Configuration par défaut
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
            UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', 'instance/uploads'),
            OUTPUT_FOLDER=os.getenv('OUTPUT_FOLDER', 'instance/output'),
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max-limit
            QUALITY=int(os.getenv('QUALITY', '75'))
        )

    # Création des dossiers nécessaires
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

    # Enregistrement des blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app