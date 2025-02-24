import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_service_logger():
    """Configure le logger pour les services"""
    logger = logging.getLogger("app.services")

    if not logger.handlers:
        # Création du format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler pour le fichier
        log_dir = Path(__file__).parent.parent.parent / "logs"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_dir / "services.log", maxBytes=1024 * 1024, backupCount=5  # 1MB
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)

    return logger


# Création du logger
service_logger = setup_service_logger()
