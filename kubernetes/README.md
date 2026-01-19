# Kubernetes

Cette partie du projet concerne le déploiement de l’application sur Kubernetes.

L’objectif est de vérifier la bonne compréhension des objets Kubernetes
de base et le bon fonctionnement du cluster.

---

## Objectif

Pour cette étape, nous avons mis en place un déploiement Kubernetes minimal
conformément aux exigences du projet :

- Un namespace dédié au binôme
- Un ReplicaSet pour le frontend
- Un Service pour exposer le frontend
- Un pod en état Running
- Un test fonctionnel simple

---

## Namespace

Un namespace nommé `victor-leopold` est utilisé afin d’isoler les ressources
du binôme dans le cluster Kubernetes.

Fichier :
- "namespace.yaml"


## Frontend (v1)

Le frontend est déployé à l’aide d’un ReplicaSet contenant un seul pod.

Pour cette version, une image `nginx:alpine` est utilisée afin de valider
le fonctionnement de Kubernetes sans dépendre de l’application finale.

Fichier :
- "frontend-replicaset.yaml"

Les ressources CPU et mémoire sont volontairement limitées, conformément
aux consignes du sujet.


## Service

Un Service de type `NodePort` permet d’exposer le frontend et de fournir
une adresse stable pour accéder au pod.

Fichier :
- "frontend-service.yaml"


## Déploiement

Les commandes suivantes ont été utilisées pour déployer les ressources :

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/frontend-replicaset.yaml
kubectl apply -f kubernetes/frontend-service.yaml
