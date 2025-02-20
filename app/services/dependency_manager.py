import subprocess
import sys
import importlib.metadata as metadata
import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)

class DependencyManager:
    """Gère les dépendances de l'application"""
    
    REQUIRED_PACKAGES = {
        'flask': '3.0.2',
        'flask-wtf': '1.2.1',
        'pillow': '11.1.0',
        'werkzeug' :'3.1.3',
        'pytest': '8.0.1',
        'pytest-flask': '1.3.0',
        'black': '22.3.0',
        'flake8': '4.0.1',
        'pdf2image': '1.18.5',
        'python-docx': '0.8.11',
        'reportlab': '4.1.0',
        'pypdf2': '3.0.1',
        'pymupdf': '1.23.7',
        'python-dotenv': '1.0.1',
        'python-magic': '0.4.27',
    }

    @classmethod
    def check_dependencies(cls) -> List[Tuple[str, str, str]]:
        """
        Vérifie les versions des dépendances installées
        Retourne une liste de tuples (package, version_installée, version_requise)
        """
        missing_or_outdated = []
        
        for package, required_version in cls.REQUIRED_PACKAGES.items():
            try:
                installed_version = pkg_resources.get_distribution(package).version
                if installed_version != required_version:
                    missing_or_outdated.append((package, installed_version, required_version))
            except pkg_resources.DistributionNotFound:
                missing_or_outdated.append((package, None, required_version))
        
        return missing_or_outdated

    @classmethod
    def install_dependencies(cls) -> bool:
        """Installe ou met à jour les dépendances manquantes"""
        try:
            missing = cls.check_dependencies()
            if not missing:
                logger.info("Toutes les dépendances sont à jour")
                return True

            logger.info("Installation des dépendances manquantes...")
            requirements_file = Path('requirements.txt')
            
            # Création du fichier requirements.txt temporaire
            with open(requirements_file, 'w') as f:
                for package, _, version in missing:
                    f.write(f"{package}=={version}\n")

            # Installation des dépendances
            subprocess.check_call([
                sys.executable, 
                '-m', 
                'pip', 
                'install', 
                '-r', 
                str(requirements_file)
            ])

            logger.info("Dépendances installées avec succès")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'installation des dépendances: {e}")
            return False

    @classmethod
    def get_dependency_status(cls) -> dict:
        """Retourne l'état des dépendances"""
        status = {
            'total': len(cls.REQUIRED_PACKAGES),
            'installed': 0,
            'missing': 0,
            'outdated': 0,
            'details': []
        }

        for package, installed_version, required_version in cls.check_dependencies():
            if installed_version is None:
                status['missing'] += 1
                state = 'missing'
            elif installed_version != required_version:
                status['outdated'] += 1
                state = 'outdated'
            else:
                status['installed'] += 1
                state = 'ok'

            status['details'].append({
                'package': package,
                'installed': installed_version,
                'required': required_version,
                'state': state
            })

        return status