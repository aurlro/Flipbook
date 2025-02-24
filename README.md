# Flipbook Project

Un visualisateur de flipbook interactif en JavaScript.

## Installation

1. Cloner le repository:
   ```bash
   git clone [url-du-repo]

   # Intégration de Flask 3.0

## Description
Cette PR ajoute une interface web avec Flask 3.0 au projet Flipbook.

## Changements
- Ajout de l'application Flask avec routes API
- Création des templates base et index
- Système d'upload de fichiers
- Tests Flask
- Configuration du dossier upload

## Tests
- [x] Tests unitaires ajoutés pour Flask
- [x] Tests manuels effectués
- [x] Vérification des uploads
- [x] Validation des formats de fichiers

## TODO
- [ ] Ajouter la pagination
- [ ] Améliorer la gestion des erreurs
- [ ] Ajouter la documentation API
- [ ] Optimiser le chargement des images

## Comment tester
1. Installer les dépendances : `pip install -e ".[dev]"`
2. Lancer les tests : `python -m pytest tests/ -v`
3. Lancer l'application : `flask run`
4. Ouvrir http://localhost:5000
5. Tester l'upload d'images
