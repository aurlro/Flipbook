@echo off
echo Création de l'environnement virtuel...
python -m venv venv

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Installation des dépendances...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Vérification des installations...
python -c "import flask; print('Flask version:', flask.__version__)"
python -c "import flask_wtf; print('Flask-WTF installé avec succès')"

echo Installation terminée !
pause