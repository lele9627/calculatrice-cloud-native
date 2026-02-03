# Application – Calculatrice Web

Cette partie contient le backend (API Flask), le frontend (HTML/CSS/JS) et
les Dockerfiles utilisés pour la conteneurisation.

## Structure

- `app.py` : API Flask (jobs asynchrones via RabbitMQ + Redis)
- `consumer.py` : worker qui consomme les jobs et écrit le résultat
- `index.html`, `css/`, `js/` : frontend statique
- `Dockerfile.backend`, `Dockerfile.consumer`, `Dockerfile.frontend`
- `nginx.conf` : proxy `/api` vers le backend

## API

### POST `/api/calc`
Reçoit une expression (ex: `"2+3"`), crée un job et retourne un ID.

Exemple de requête :
```json
{"expression":"12*(3+4)"}
```

Exemple de réponse :
```json
{"id":"<uuid>","status":"queued"}
```

### GET `/api/result/<id>`
Retourne le résultat quand le job est terminé.

### Health checks
- `GET /api/health/redis`
- `GET /api/health/rabbit`

## Lancement local (backend sans Docker)

Prérequis : Python 3.10+
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Images Docker

Backend :
```bash
docker build -t calculatrice-backend -f application/Dockerfile.backend application
```

Consumer :
```bash
docker build -t calculatrice-consumer -f application/Dockerfile.consumer application
```

Frontend :
```bash
docker build -t calculatrice-frontend -f application/Dockerfile.frontend application
```
