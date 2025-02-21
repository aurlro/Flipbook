import sys
import os
import site

def check_environment():
    print("=== Informations sur l'environnement Python ===")
    print(f"Version Python: {sys.version}")
    print(f"\nChemin Python: {sys.executable}")
    print(f"\nVariable PATH: {os.environ.get('PATH')}")
    
    print("\n=== Site Packages ===")
    for path in site.getsitepackages():
        print(f"\nContenu de {path}:")
        try:
            files = os.listdir(path)
            for f in files:
                if f.endswith('.dist-info') or f.endswith('.egg-info'):
                    print(f"  - {f}")
        except Exception as e:
            print(f"  Erreur: {e}")

if __name__ == "__main__":
    check_environment()