import os
from pathlib import Path

from flask import Flask


def create_app():
    # Créez l'instance Flask
    app = Flask(__name__)

    # Configuration
    app.config.update(
        MAX_CONTENT_LENGTH=50 * 1024 * 1024,  # 50MB max-limit
        UPLOAD_FOLDER=Path(app.static_folder) / "uploads",
        PDF_FOLDER=Path(app.static_folder) / "pdf_pages",
        ALLOWED_EXTENSIONS={"pdf", "png", "jpg", "jpeg", "gif"},
        SECRET_KEY="dev",  # À changer en production
        DEBUG=True,
    )

    # Créer les dossiers nécessaires
    for folder in [app.config["UPLOAD_FOLDER"], app.config["PDF_FOLDER"]]:
        folder.mkdir(parents=True, exist_ok=True)

    # Enregistrez les routes
    from .app import bp

    app.register_blueprint(bp)

    return app
