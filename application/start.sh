#!/bin/sh
set -e

echo "Démarrage du backend Flask"

# Lancer Flask directement (le container est l'environnement)
exec python app.py

