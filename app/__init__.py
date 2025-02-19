from flask import Flask
import os
from .config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config[config_name])
    
    # Création des dossiers nécessaires
    os.makedirs(app.config['PDF_SOURCE'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    # Enregistrement des blueprints
    from .routes.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
