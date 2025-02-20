import sys
import os
import logging
import subprocess
import venv
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Ajout sécurisé du chemin du module
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / 'app'))

def setup_venv():
    """Crée et configure l'environnement virtuel"""
    venv_dir = BASE_DIR / 'venv'
    if not venv_dir.exists():
        print("Création de l'environnement virtuel...")
        venv.create(venv_dir, with_pip=True)
        
        # Détermination du chemin de l'interpréteur Python dans le venv
        if sys.platform == 'win32':
            python_path = venv_dir / 'Scripts' / 'python.exe'
            pip_path = venv_dir / 'Scripts' / 'pip.exe'
        else:
            python_path = venv_dir / 'bin' / 'python'
            pip_path = venv_dir / 'bin' / 'pip'

        # Mise à jour de pip
        subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
        
        # Installation des dépendances
        requirements_path = BASE_DIR / 'requirements.txt'
        if requirements_path.exists():
            print("Installation des dépendances...")
            subprocess.run([str(pip_path), 'install', '-r', str(requirements_path)], check=True)
        
        return str(python_path)
    
    # Retourne le chemin de l'interpréteur Python du venv existant
    return str(venv_dir / ('Scripts' if sys.platform == 'win32' else 'bin') / ('python.exe' if sys.platform == 'win32' else 'python'))

def setup_logging():
    """Configure le système de logging de manière sécurisée"""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(mode=0o750, exist_ok=True)
    log_file = log_dir / 'flipbook.log'
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,
        backupCount=5,
        mode='a',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

def setup():
    """Configuration initiale sécurisée de l'application"""
    try:
        # Configuration du logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Démarrage de l'application Flipbook")
        
        # Création/vérification de l'environnement virtuel
        python_path = setup_venv()
        logger.info(f"Utilisation de l'environnement Python: {python_path}")
        
        # Import des dépendances après leur installation
        from app import create_app
        from app.services.dependency_manager import DependencyManager
        from config.config import config
        
        # Vérification de l'environnement
        env = os.getenv('FLASK_ENV', 'production')
        if env not in config:
            logger.error("Configuration d'environnement invalide")
            return False
        
        # Vérification finale des dépendances
        if not DependencyManager.install_dependencies():
            logger.error("Erreur lors de la vérification des dépendances")
            return False
        
        return True
        
    except Exception as e:
        logging.error(f"Erreur lors de la configuration: {str(e)}")
        return False

def get_server_config():
    """Récupère la configuration sécurisée du serveur"""
    env = os.getenv('FLASK_ENV', 'production')
    return {
        'host': os.getenv('FLASK_HOST', '127.0.0.1'),
        'port': int(os.getenv('FLASK_PORT', 5000)),
        'debug': env == 'development',
        'ssl_context': 'adhoc' if env == 'production' else None
    }

if __name__ == '__main__':
    try:
        if not setup():
            sys.exit(1)
        
        # Import des modules nécessaires après la configuration
        from app import create_app
        from config.config import config
        
        env = os.getenv('FLASK_ENV', 'production')
        app = create_app(config[env])
        server_config = get_server_config()
        
        if env == 'production':
            server_config['debug'] = False
        
        app.run(**server_config)
        
    except Exception as e:
        logging.error(f"Erreur fatale lors du démarrage: {str(e)}")
        sys.exit(1)