@echo off
setlocal

:: Vérification de l'environnement virtuel
if not exist "venv" (
    echo Erreur: Environnement virtuel non trouvé.
    echo Exécutez d'abord setup.bat pour installer l'application.
    pause
    exit /b 1
)

:: Configuration de l'environnement
set FLASK_ENV=development
set FLASK_HOST=127.0.0.1
set FLASK_PORT=5000

:: Activation de l'environnement virtuel et lancement
call venv\Scripts\activate.bat
python run.py
pause