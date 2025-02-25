# Structure des branches Git pour Flipbook

## Branches principales

### `main`
- Branche de production stable
- Protégée contre les pushs directs
- Merge uniquement via Pull Request
- Tests obligatoires

### `develop`
- Branche de développement principale
- Base pour toutes les nouvelles fonctionnalités
- Merge via Pull Request
- Tests requis

## Branches de travail

### `feature/*`
- Pour les nouvelles fonctionnalités
- Nomenclature : feature/nom-fonctionnalite
- Créée depuis : develop
- Merge vers : develop

### `bugfix/*`
- Pour les corrections de bugs non-urgents
- Nomenclature : bugfix/description-bug
- Créée depuis : develop
- Merge vers : develop

### `hotfix/*`
- Pour les corrections urgentes en production
- Nomenclature : hotfix/description-correction
- Créée depuis : main
- Merge vers : main et develop

### `release/*`
- Pour la préparation des releases
- Nomenclature : release/v1.x.x
- Créée depuis : develop
- Merge vers : main et develop

## Workflow de développement

1. Pour une nouvelle fonctionnalité :
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/ma-fonctionnalite
   # Développement...
   git push origin feature/ma-fonctionnalite
   # Créer une Pull Request vers develop