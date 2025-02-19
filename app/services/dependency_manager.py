import subprocess
import sys
import pkg_resources
import os

class DependencyManager:
    @staticmethod
    def get_required_packages():
        """Lit les dépendances depuis requirements.txt"""
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'requirements.txt')
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]

    @staticmethod
    def check_dependencies():
        """Vérifie si toutes les dépendances sont installées"""
        required = DependencyManager.get_required_packages()
        installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        
        missing = []
        outdated = []
        
        for req in required:
            if '==' in req:
                package_name, required_version = req.split('==')
                if package_name.lower() not in installed:
                    missing.append(req)
                elif installed[package_name.lower()] != required_version:
                    outdated.append(req)
            else:
                if req.lower() not in installed:
                    missing.append(req)
        
        return missing, outdated

    @staticmethod
    def install_dependencies():
        """Installe les dépendances manquantes"""
        missing, outdated = DependencyManager.check_dependencies()
        
        if not missing and not outdated:
            print("Toutes les dépendances sont déjà installées et à jour.")
            return True

        print("Installation/Mise à jour des dépendances...")
        
        try:
            # Mise à jour de pip
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            
            # Installation des packages
            packages_to_install = missing + outdated
            if packages_to_install:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages_to_install)
            
            print("Installation des dépendances terminée avec succès.")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation des dépendances: {str(e)}")
            return False
