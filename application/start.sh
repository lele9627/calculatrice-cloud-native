#!/bin/bash
set -e

echo "Démarrage de la calculatrice (Flask + RabbitMQ consumer)"

# Vérifier venv
if [ ! -d ".venv" ]; then
  echo "Erreur : venv .venv introuvable"
  echo "Créez-la avec : python3 -m venv .venv"
  exit 1
fi

# Activer venv
source .venv/bin/activate

# Installer dépendances
python -m pip install -r requirements.txt >/dev/null

# Lancer le consumer RabbitMQ en arrière-plan
export SIMULATE_LATENCY=0  # Pas de latence simulée

echo "→ Lancement du consumer RabbitMQ (latence = ${SIMULATE_LATENCY}s)"
python consumer.py &

CONSUMER_PID=$!
echo "   Consumer PID = $CONSUMER_PID"

# S'assurer que le consumer s'arrête quand on quitte
trap "echo 'Arrêt du consumer'; kill $CONSUMER_PID" EXIT

# Lancer Flask (au premier plan)
echo "→ Lancement du serveur Flask sur http://127.0.0.1:5001"
echo "Ctrl+C pour arrêter"
echo "----------------------------------------"

python app.py
