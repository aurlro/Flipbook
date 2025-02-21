import subprocess
import sys
import platform
from pathlib import Path

def check_visual_studio():
    """Vérifie si Visual Studio Build Tools est installé"""
    vs_path = Path(r"C:\Program Files (x86)\Microsoft Visual Studio")
    if not vs_path.exists():
        print("Visual Studio Build Tools n'est pas installé.")
        print("Veuillez exécuter setup_windows.bat d'abord.")
        return False
    return True

def install_requirements():
    """Installation des dépendances avec gestion d'erreur"""
    try:
        # Installation des dépendances de base
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Installation des dépendances principales
        subprocess.run([
            sys.executable, 
            "-m", 
            "pip", 
            "install",
            "-r", 
            "requirements.txt"
        ], check=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation: {e}")
        print(f"Code de sortie: {e.returncode}")
        if e.output:
            print(f"Sortie: {e.output.decode()}")
        return False

def main():
    """Programme principal"""
    if platform.system() == "Windows":
        if not check_visual_studio():
            sys.exit(1)
    
    if not install_requirements():
        sys.exit(1)
    
    print("Installation des dépendances terminée avec succès!")

if __name__ == "__main__":
    main()