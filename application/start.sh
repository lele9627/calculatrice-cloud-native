#!/bin/bash

# Script pour démarrer la calculatrice Flask

echo " Démarrage de la calculatrice Flask..."

//Vérifier si Flask est installé
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installation de Flask..."
    pip3 install -r requirements.txt
fi

echo " Lancement du serveur sur http://127.0.0.1:5000"
echo " Appuyez sur Ctrl+C pour arrêter le serveur"
echo " Victor Olivier et Leopard Saublet vous remercie pour votre usage de nottre calculatrice !"
echo " ----------------------------------------"

python3 app.py