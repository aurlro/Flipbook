import subprocess
import sys
import pkg_resources
import os
import logging

class DependencyManager:
    @staticmethod
    def get_required_packages():
        """Lit les dépendances depuis requirements.txt"""
        try:
            requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'requirements.txt')
            if not os.path.exists(requirements_path):
                logging.error(f"Le fichier requirements.txt n'existe pas à l'emplacement : {requirements_path}")
                return []
                
            with open(requirements_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            logging.error(f"Erreur lors de la lecture de requirements.txt: {str(e)}")
            return []

    @staticmethod
    def check_dependencies():
        """Vérifie si toutes les dépendances sont installées"""
        required = DependencyManager.get_required_packages()
        if not required:
            logging.warning("Aucune dépendance trouvée dans requirements.txt")
            return [], []

        installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        
        missing = []
        outdated = []
        
        for req in required:
            try:
                if '==' in req:
                    package_name, required_version = req.split('==')
                    package_name = package_name.lower()
                    if package_name not in installed:
                        missing.append(req)
                    elif installed[package_name] != required_version:
                        outdated.append(req)
                else:
                    package_name = req.lower()
                    if package_name not in installed:
                        missing.append(req)

            except Exception as e:
                logging.error(f"Erreur lors de la vérification de la dépendance {req}: {str(e)}")
        
        return missing, outdated

    @staticmethod
    def install_dependencies():
        """Installe les dépendances manquantes"""
        missing, outdated = DependencyManager.check_dependencies()
        
        if not missing and not outdated:
            logging.info("Toutes les dépendances sont déjà installées et à jour.")
            return True

        logging.info("Installation/Mise à jour des dépendances...")
        
        try:
            # Mise à jour de pip
            logging.info("Mise à jour de pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE)
            
            # Installation des packages
            packages_to_install = missing + outdated
            if packages_to_install:
                logging.info(f"Installation des packages: {', '.join(packages_to_install)}")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages_to_install,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.PIPE)
            
            logging.info("Installation des dépendances terminée avec succès.")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur lors de l'installation des dépendances: {e.stderr.decode() if e.stderr else str(e)}")
            return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'installation des dépendances: {str(e)}")
            return False
