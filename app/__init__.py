from flask import Flask
from config.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enregistrement des blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # Création des dossiers nécessaires
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    return app