# Kubernetes

Manifests Kubernetes pour déployer la calculatrice complète :
frontend, backend, Redis, RabbitMQ et consumer.

## Pré-requis

- Accès au cluster via `kubectl` (kubeconfig fourni par l'enseignant)
- Ingress controller Nginx déjà installé sur le cluster

## Déploiement

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/redis-deployment.yaml
kubectl apply -f kubernetes/redis-service.yaml
kubectl apply -f kubernetes/rabbitmq-deployment.yaml
kubectl apply -f kubernetes/rabbitmq-service.yaml
kubectl apply -f kubernetes/backend-replicaset.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/consumer-deployment.yaml
kubectl apply -f kubernetes/frontend-replicaset.yaml
kubectl apply -f kubernetes/frontend-service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## Vérification

```bash
kubectl get pods -n victor-leopold
kubectl get svc -n victor-leopold
kubectl get ingress -n victor-leopold
```

## Accès

Le trafic passe par l'Ingress :

`http://calculatrice-victor-leopold.polytech-dijon.kiowy.net`

## Images Docker

Les images doivent être poussées en `linux/amd64` pour le cluster GKE.

Exemple :
```bash
docker buildx build --platform linux/amd64 \
  -t lele9627/calculatrice-backend:v4 \
  -f application/Dockerfile.backend application \
  --push
```
