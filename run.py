import sys
import os
import logging

# Ajoutez le chemin du module au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app
from app.services.dependency_manager import DependencyManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configuration de l'environnement
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', '1')

def setup():
    """Configuration initiale de l'application"""
    # Log des informations de débogage
    logging.info(f"Current working directory: {os.getcwd()}")
    logging.info(f"Python path: {sys.path}")
    
    # Vérification et installation des dépendances Python
    if not DependencyManager.install_dependencies():
        logging.error("Erreur: Impossible d'installer toutes les dépendances requises.")
        return False
    return True

if __name__ == '__main__':
    if setup():
        # Création de l'application avec la configuration appropriée
        app = create_app(os.getenv('FLASK_ENV'))
        
        # Démarrage du serveur
        app.run(
            debug=True,
            host='0.0.0.0',  # Permet l'accès depuis d'autres machines
            port=5000
        )
    else:
        logging.error("L'application n'a pas pu démarrer à cause d'erreurs dans la configuration.")
