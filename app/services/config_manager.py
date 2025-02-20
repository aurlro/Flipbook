from pathlib import Path
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConfigManager:
    """Gère la configuration de l'application"""
    
    def __init__(self, config_file: Path = None):
        self.config_file = config_file or Path('instance/config.json')
        self._config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Charge la configuration depuis le fichier"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
                logger.info("Configuration chargée avec succès")
            else:
                self._config = self.get_default_config()
                self.save_config()
                logger.info("Configuration par défaut créée")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {e}")
            self._config = self.get_default_config()

    def save_config(self) -> None:
        """Sauvegarde la configuration dans le fichier"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=4)
            logger.info("Configuration sauvegardée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {e}")

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            'quality': 75,
            'output_format': 'png',
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'allowed_extensions': ['pdf'],
            'conversion_timeout': 300,  # 5 minutes
            'cleanup_interval': 86400  # 24 heures
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Définit une valeur de configuration"""
        self._config[key] = value
        self.save_config()