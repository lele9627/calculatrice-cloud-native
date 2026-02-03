# Calculatrice Cloud Native

Projet de calculatrice web déployée sur Kubernetes, avec backend API Flask,
frontend statique Nginx, Redis, RabbitMQ et un consumer asynchrone.

## Auteurs

- Léopold SAUBLET (GitHub: lele9627)
- Victor OLIVIER (GitHub: Victor3699)

## Structure

- `application/` : API Flask, frontend HTML/CSS/JS, Dockerfiles
- `kubernetes/` : manifests de déploiement Kubernetes
- `foundation/` : Terraform pour l'infrastructure (Scaleway)

## Démarrage rapide (Docker local)

Construire les images :
```bash
docker build -t calculatrice-backend -f application/Dockerfile.backend application
docker build -t calculatrice-consumer -f application/Dockerfile.consumer application
docker build -t calculatrice-frontend -f application/Dockerfile.frontend application
```

Lancer les services :
```bash
docker network create calculatrice-net
docker run -d --name redis-service --network calculatrice-net redis:7
docker run -d --name rabbitmq-service --network calculatrice-net rabbitmq:3-management

docker run -d --name backend-service --network calculatrice-net \
  -e REDIS_HOST=redis-service -e REDIS_PORT=6379 \
  -e RABBIT_HOST=rabbitmq-service -e RABBIT_PORT=5672 -e RABBIT_QUEUE=calc_jobs \
  calculatrice-backend

docker run -d --name consumer --network calculatrice-net \
  -e REDIS_HOST=redis-service -e REDIS_PORT=6379 \
  -e RABBIT_HOST=rabbitmq-service -e RABBIT_PORT=5672 -e RABBIT_QUEUE=calc_jobs \
  calculatrice-consumer

docker run -d --name frontend --network calculatrice-net -p 8080:80 calculatrice-frontend
```

Accès frontend : `http://localhost:8080`

## Déploiement Kubernetes

Voir `kubernetes/README.md` pour les commandes de déploiement, et
`foundation/README.md` pour l'infrastructure Terraform.
