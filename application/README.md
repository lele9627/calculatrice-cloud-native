# Application – Calculatrice Web

Cette partie du projet correspond à l’application de calculatrice web.

L’application est composée d’un frontend en HTML, CSS et JavaScript et d’un backend
en Python utilisant Flask pour exposer une API REST.

---

## Description

La calculatrice permet à un utilisateur de saisir une expression mathématique
via une interface web. Le calcul est réalisé côté serveur par l’API Flask,
qui renvoie le résultat au frontend.

---

## Structure actuelle

application/
├── index.html
├── css/
├── js/
├── app.py
├── requirements.txt
├── start.sh
├── Dockerfile.frontend
└── README.md

---

## Frontend

* Développé en HTML, CSS et JavaScript
* Permet de saisir une expression mathématique
* Envoie la requête de calcul vers l’API backend
* Le frontend a été conteneurisé avec Docker à l’aide d’une image Nginx

---

## Backend

* API développée en Python avec Flask
* Expose un endpoint `/api/calc`
* Réalise les calculs côté serveur

### Endpoint

POST /api/calc

### Exemple de requête

```json
{
  "expression": "12*(3+4)"
}
```

### Exemple de réponse

```json
{
  "result": 84
}
```

### Erreurs possibles

* Division par zéro
* Expression invalide

### Opérateurs supportés

* * * /  ^  ( )

---

## Lancement en local (backend)

### Prérequis

* Python 3.10 ou supérieur

### Commande

```bash
./start.sh
```

Accès :
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Conteneurisation du frontend

### Construction de l’image Docker

```bash
docker build -t calculatrice-frontend -f application/Dockerfile.frontend application
```

### Lancement en local

```bash
docker run -p 8080:80 calculatrice-frontend
```

Accès :
[http://localhost:8080/](http://localhost:8080/)

Le frontend s’affiche correctement. Le message d’erreur de connexion est normal
tant que le backend n’est pas lancé ou accessible.

---

## Auteurs

Victor Olivier
Léopold Saublet
