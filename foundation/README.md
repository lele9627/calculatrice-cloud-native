# Infrastructure Terraform -- Calculatrice

Ce projet Terraform déploie l'infrastructure cloud nécessaire à
l'application Calculatrice sur Scaleway.

------------------------------------------------------------------------

## Ressources déployées

-   Namespace Scaleway Container Registry
-   Cluster Kubernetes (Kapsule) avec CNI Cilium
-   Instance PostgreSQL 15 (RDB)
-   Load Balancer Scaleway
-   Enregistrement DNS (A record)

------------------------------------------------------------------------

## Variables

  Variable       Description       Valeur par défaut
  -------------- ----------------- -------------------
  project_name   Nom du projet     calculatrice
  binome_1       Binôme 1          victor
  binome_2       Binôme 2          leopold
  region         Région Scaleway   fr-par

------------------------------------------------------------------------

## Prérequis

-   Terraform \>= 0.13
-   Compte Scaleway configuré (scw init)
-   Droits Kubernetes, Registry, RDB, Load Balancer et DNS

------------------------------------------------------------------------

## Déploiement

``` bash
terraform init
terraform plan
terraform apply
```

------------------------------------------------------------------------

## Détails techniques

-   Kubernetes version : 1.27.4
-   CNI : Cilium
-   Base de données : PostgreSQL 15
-   Type DB : db-dev-s
-   Load Balancer : LB-S
-   Le record DNS pointe par défaut vers 0.0.0.0

------------------------------------------------------------------------

## Auteurs

Léopold SAUBLET \ Victor OLIVIER
