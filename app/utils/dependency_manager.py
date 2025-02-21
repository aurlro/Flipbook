"""Module de gestion des dépendances du FlipBook."""

import logging
import subprocess
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DependencyManager:
    """Gestionnaire de dépendances pour l'application FlipBook."""

    REQUIRED_PACKAGES = {
        "PyMuPDF": "fitz",
        "Pillow": "PIL",
        "Flask": "flask",
        "Jinja2": "jinja2",
    }

    @classmethod
    def get_dependency_status(cls) -> Dict[str, int]:
        """
        Vérifie l'état des dépendances requises.

        Returns:
            Dict contenant:
                - total: Nombre total de dépendances
                - installed: Nombre de dépendances installées
                - missing: Nombre de dépendances manquantes
        """
        total = len(cls.REQUIRED_PACKAGES)
        installed = 0
        missing = []

        for package_name, import_name in cls.REQUIRED_PACKAGES.items():
            try:
                pkg_resources.get_distribution(package_name)
                installed += 1
            except pkg_resources.DistributionNotFound:
                missing.append(package_name)
                logger.warning(f"Dépendance manquante : {package_name}")

        return {
            "total": total,
            "installed": installed,
            "missing": len(missing),
            "missing_packages": missing,
        }

    @classmethod
    def check_system_dependencies(cls) -> Tuple[bool, List[str]]:
        """
        Vérifie les dépendances système nécessaires.

        Returns:
            Tuple contenant:
                - bool: True si toutes les dépendances sont présentes
                - List[str]: Liste des dépendances manquantes
        """
        missing_deps = []

        # Vérification de ghostscript (nécessaire pour certains PDFs)
        if not cls._check_ghostscript():
            missing_deps.append("ghostscript")

        return len(missing_deps) == 0, missing_deps

    @staticmethod
    def _check_ghostscript() -> bool:
        """
        Vérifie si Ghostscript est installé sur le système.

        Returns:
            bool: True si Ghostscript est disponible
        """
        try:
            subprocess.run(
                ["gs", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("Ghostscript n'est pas installé sur le système")
            return False

    @classmethod
    def install_missing_packages(
        cls, packages: Optional[List[str]] = None
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Installe les packages Python manquants.

        Args:
            packages: Liste des packages à installer,
                     si None, installe les packages manquants

        Returns:
            Tuple contenant:
                - bool: True si l'installation est réussie
                - List[str]: Packages installés avec succès
                - List[str]: Packages dont l'installation a échoué
        """
        if packages is None:
            status = cls.get_dependency_status()
            packages = status.get("missing_packages", [])

        if not packages:
            return True, [], []

        successful = []
        failed = []

        for package in packages:
            try:
                subprocess.run(
                    ["pip", "install", package],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                successful.append(package)
                logger.info(f"Package installé avec succès : {package}")
            except subprocess.CalledProcessError as e:
                failed.append(package)
                logger.error(
                    f"Échec de l'installation de {package}. " f"Erreur : {e.stderr}"
                )

        return len(failed) == 0, successful, failed

    @classmethod
    def check_and_install(cls) -> bool:
        """
        Vérifie et installe automatiquement les dépendances manquantes.

        Returns:
            bool: True si toutes les dépendances sont satisfaites
        """
        # Vérification des dépendances système
        system_ok, missing_system = cls.check_system_dependencies()
        if not system_ok:
            logger.error(
                "Dépendances système manquantes : " f"{', '.join(missing_system)}"
            )
            return False

        # Vérification et installation des packages Python
        status = cls.get_dependency_status()
        if status["missing"] > 0:
            success, installed, failed = cls.install_missing_packages()
            if not success:
                logger.error(
                    "Échec de l'installation des packages : " f"{', '.join(failed)}"
                )
                return False

        return True
