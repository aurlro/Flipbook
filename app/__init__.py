from flask import Flask
from config.config import config  # Importation du dictionnaire de configuration
import os
from pathlib import Path


def create_app(config_name="default"):
    """Crée et configure l'instance de l'application Flask"""

    app = Flask(__name__)

    # Utilisation correcte de la configuration
    app.config.from_object(config[config_name])

    # Initialisation de la configuration
    config[config_name].init_app(app)

    # Enregistrement des blueprints
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
