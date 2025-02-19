import sys
import os
print(sys.path)
print(os.getcwd())
from app import create_app
from app.services.dependency_manager import DependencyManager

def setup():
    """Configuration initiale de l'application"""
    # Vérification et installation des dépendances Python
    if not DependencyManager.install_dependencies():
        print("Erreur: Impossible d'installer toutes les dépendances requises.")
        return False
    return True

if __name__ == '__main__':
    if setup():
        app = create_app()
        app.run(debug=True)
    else:
        print("L'application n'a pas pu démarrer à cause d'erreurs dans la configuration.")
