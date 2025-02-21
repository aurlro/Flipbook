@echo off
mkdir app\static\css
mkdir app\static\js
mkdir instance\uploads
mkdir instance\output
mkdir instance\temp
mkdir logs
mkdir tests

setlocal enabledelayedexpansion

echo === Installation de Flipbook ===
echo.

:: Vérification de Python
python --version > nul 2>&1
if errorlevel 1 (
    echo Erreur: Python n'est pas installé.
    echo Veuillez installer Python 3.8 ou supérieur.
    pause
    exit /b 1
)

:: Création de l'environnement virtuel
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo Erreur lors de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
)

:: Activation de l'environnement virtuel
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Erreur lors de l'activation de l'environnement virtuel.
    pause
    exit /b 1
)

:: Mise à jour de pip
echo Mise à jour de pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Erreur lors de la mise à jour de pip.
    pause
    exit /b 1
)

:: Installation des dépendances
echo Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo Erreur lors de l'installation des dépendances.
    pause
    exit /b 1
)

echo.
echo Installation terminée avec succès !
echo Pour lancer l'application, utilisez run.bat
pause