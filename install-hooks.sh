#!/bin/sh

# Couleurs pour une meilleure lisibilité
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${YELLOW}📥 Installation des hooks Git...${NC}"

# Créer le dossier des hooks si nécessaire
mkdir -p .git/hooks

# Copier tous les hooks
cp .githooks/* .git/hooks/

# Rendre les hooks exécutables
chmod +x .git/hooks/*

echo "${GREEN}✅ Hooks Git installés avec succès !${NC}"
