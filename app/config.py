import os
from dotenv import load_dotenv

# Obtenir le chemin de base et charger les variables d'environnement
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Chemin de base de l'application
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Configuration Flipbook
    PDF_SOURCE = os.environ.get('PDF_SOURCE') or os.path.join(BASE_DIR, 'app', 'uploads')
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER') or os.path.join(BASE_DIR, 'app', 'output')
    QUALITY = os.environ.get('QUALITY', 100)  # Valeur par défaut: 100

    # Assurez-vous que QUALITY est un entier
    if isinstance(QUALITY, str):
        if QUALITY.lower() == 'high':
            QUALITY = 100
        elif QUALITY.lower() == 'medium':
            QUALITY = 75
        elif QUALITY.lower() == 'low':
            QUALITY = 50
        else:
            try:
                QUALITY = int(QUALITY)
            except ValueError:
                QUALITY = 100  # Valeur par défaut si la conversion échoue

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Dictionnaire pour sélectionner la configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
