# Foundation – Terraform

Déploiement de l'infrastructure cloud nécessaire à l'application Calculatrice
sur Scaleway (registry, cluster Kubernetes, base de données, load balancer, DNS).

## Pré-requis

- Terraform >= 0.13
- `scw` configuré avec un compte Scaleway
- Droits Kubernetes, Registry, RDB, Load Balancer et DNS

## Déploiement

```bash
terraform init
terraform plan
terraform apply
```

## Variables

- `project_name` (défaut: `calculatrice`)
- `binome_1` (défaut: `victor`)
- `binome_2` (défaut: `leopold`)
- `region` (défaut: `fr-par`)

## Ressources créées

- Namespace Scaleway Container Registry
- Cluster Kubernetes (Kapsule) avec Cilium
- Instance PostgreSQL 15 (RDB)
- Load Balancer Scaleway
- Enregistrement DNS (A record)
