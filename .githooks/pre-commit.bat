@echo off
setlocal enabledelayedexpansion

REM Activation de l'environnement virtuel
call venv\Scripts\activate.bat

echo 🔍 Démarrage des vérifications pre-commit...

REM Vérification du formatage Python
echo 📝 Vérification du formatage avec black...
black --check .
if !errorlevel! neq 0 (
    echo ❌ Erreur de formatage. Exécutez 'black .' pour corriger
    exit /b 1
)

REM Vérification des imports
echo 📦 Vérification des imports avec isort...
isort --check-only .
if !errorlevel! neq 0 (
    echo ❌ Imports mal ordonnés. Exécutez 'isort .' pour corriger
    exit /b 1
)

REM Linting avec flake8
echo 🔍 Vérification du style avec flake8...
python -m flake8
if !errorlevel! neq 0 (
    echo ❌ Erreurs de style détectées
    exit /b 1
)

REM Tests avec pytest
echo 🧪 Exécution des tests avec pytest...
pytest
if !errorlevel! neq 0 (
    echo ❌ Certains tests ont échoué
    exit /b 1
)

REM Désactivation de l'environnement virtuel
deactivate

echo ✅ Toutes les vérifications sont passées!
exit /b 0