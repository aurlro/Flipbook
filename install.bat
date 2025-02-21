@echo off
echo Configuration de l'environnement Flipbook...

REM Vérification de Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.11 ou superieur
    pause
    exit /b 1
)

REM Création de l'environnement virtuel si nécessaire
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activation de l'environnement virtuel
call venv\Scripts\activate.bat

REM Installation des dépendances
echo Installation des dependances...
python scripts\install_dependencies.py

if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'installation des dependances.
    pause
    exit /b 1
)

echo Configuration terminee avec succes!
echo Pour demarrer l'application:
echo 1. Activez l'environnement virtuel: call venv\Scripts\activate.bat
echo 2. Lancez l'application: python run.py
pause