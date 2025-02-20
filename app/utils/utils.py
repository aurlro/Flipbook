import os
from pathlib import Path
from typing import List, Union
from werkzeug.utils import secure_filename
import shutil

def clean_directory(directory: Union[str, Path], max_age: int = 86400) -> List[Path]:
    """
    Nettoie les fichiers plus vieux que max_age secondes
    Retourne la liste des fichiers supprimés
    """
    directory = Path(directory)
    deleted_files = []
    
    if not directory.exists():
        return deleted_files

    for item in directory.iterdir():
        if item.is_file() and (time.time() - item.stat().st_mtime) > max_age:
            item.unlink()
            deleted_files.append(item)
        elif item.is_dir():
            try:
                shutil.rmtree(item)
                deleted_files.append(item)
            except Exception:
                continue

    return deleted_files

def get_safe_filename(filename: str) -> str:
    """Retourne un nom de fichier sécurisé"""
    return secure_filename(filename)

def ensure_directory(directory: Union[str, Path]) -> Path:
    """Crée un répertoire s'il n'existe pas et retourne son Path"""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True, mode=0o750)
    return directory