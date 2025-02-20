import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Ajout sécurisé du chemin du module
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / 'app'))

from app import create_app
from app.services.dependency_manager import DependencyManager
from config.config import config

# Configuration du logging sécurisé
def setup_logging():
    """Configure le système de logging de manière sécurisée"""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(mode=0o750, exist_ok=True)
    log_file = log_dir / 'flipbook.log'
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Rotation des logs pour éviter les problèmes d'espace disque
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        mode='a',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Configuration du logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # Éviter la double journalisation
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

def setup():
    """Configuration initiale sécurisée de l'application"""
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Log des informations de base sans exposer de détails sensibles
        logger.info("Démarrage de l'application Flipbook")
        
        # Vérification de l'environnement
        env = os.getenv('FLASK_ENV', 'production')
        if env not in config:
            logger.error("Configuration d'environnement invalide")
            return False
            
        # Vérification sécurisée des dépendances
        if not DependencyManager.install_dependencies():
            logger.error("Erreur lors de l'installation des dépendances")
            return False
            
        return True
        
    except Exception as e:
        logging.error(f"Erreur lors de la configuration: {str(e)}")
        return False

def get_server_config():
    """Récupère la configuration sécurisée du serveur"""
    env = os.getenv('FLASK_ENV', 'production')
    
    return {
        'host': os.getenv('FLASK_HOST', '127.0.0.1'),  # Localhost par défaut
        'port': int(os.getenv('FLASK_PORT', 5000)),
        'debug': env == 'development',
        'ssl_context': 'adhoc' if env == 'production' else None
    }

if __name__ == '__main__':
    try:
        if not setup():
            sys.exit(1)
            
        # Configuration de l'environnement
        env = os.getenv('FLASK_ENV', 'production')
        
        # Création de l'application
        app = create_app(config[env])
        
        # Configuration du serveur
        server_config = get_server_config()
        
        # Désactivation explicite du debugger en production
        if env == 'production':
            server_config['debug'] = False
        
        # Démarrage du serveur
        app.run(**server_config)
        
    except Exception as e:
        logging.error(f"Erreur fatale lors du démarrage: {str(e)}")
        sys.exit(1)