# Workflow Git pour Flipbook

## Branches principales

### `main`
- Branche de production
- Code stable et testé
- Déploiements automatiques
- Protected branch

### `develop`
- Branche de développement principale
- Code en cours de développement
- Base pour les features

## Branches de fonctionnalités

### `feature/*`
- Nouvelles fonctionnalités
- Nommage : `feature/nom-de-la-fonctionnalité`
- Créée depuis : `develop`
- Fusionnée vers : `develop`

### `bugfix/*`
- Corrections de bugs
- Nommage : `bugfix/description-du-bug`
- Créée depuis : `develop`
- Fusionnée vers : `develop`

### `hotfix/*`
- Corrections urgentes en production
- Nommage : `hotfix/description`
- Créée depuis : `main`
- Fusionnée vers : `main` et `develop`

## Branches spéciales

### `testing`
- Tests d'intégration
- Créée depuis : `develop`
- Mise à jour régulière

### `docs`
- Documentation du projet
- Mise à jour continue

## Workflow de développement

1. Créer une branche feature : `git checkout -b feature/ma-feature develop`
2. Développer et commiter : `git commit -m "feat: description"`
3. Mettre à jour régulièrement : `git pull origin develop`
4. Pousser les changements : `git push origin feature/ma-feature`
5. Créer une Pull Request vers `develop`
6. Après révision et tests, fusion dans `develop`
7. Suppression de la branche feature

## Conventions de commit

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactorisation
- `test:` Ajout/modification de tests
- `chore:` Maintenance

## Déploiement

1. Fusion de `develop` vers `main` via Pull Request
2. Tests automatiques
3. Review obligatoire
4. Tag de version
5. Déploiement automatique