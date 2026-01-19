# Calculatrice Web -- Flask API

Application de calculatrice web composée d'un frontend
HTML/CSS/JavaScript et d'un backend Flask exposant une API REST pour
effectuer les calculs côté serveur.

------------------------------------------------------------------------

## Structure

    TestHtml/
    ├── app.py
    ├── index.html
    ├── css/
    ├── js/
    ├── requirements.txt
    ├── start.sh
    ├── README.md

------------------------------------------------------------------------

## Lancement en local

Prérequis : Python 3.10+

``` bash
./start.sh
```

Accès : - http://127.0.0.1:5000/

------------------------------------------------------------------------

## API `/api/calc`

Requête :

``` http
POST /api/calc
Content-Type: application/json
```

``` json
{ "expression": "12*(3+4)" }
```

Réponse :

``` json
{ "result": 84 }
```

Erreurs possibles : - division par zéro - expression invalide

Opérateurs supportés : `+ - * / ^ ()`



------------------------------------------------------------------------

## Auteur

Victor Olivier et Leopard Saublet
