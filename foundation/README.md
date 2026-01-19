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
leopoldsaublet@MacBook-Air-de-Leopold calculatrice-cloud-native % terraform plan
╷
│ Error: No configuration files
│ 
│ Plan requires configuration to be present. Planning without a configuration would mark everything for destruction, which is normally not what is desired. If you would like to destroy everything, run plan
│ with the -destroy option. Otherwise, create a Terraform configuration file (.tf file) and try again.
╵
leopoldsaublet@MacBook-Air-de-Leopold calculatrice-cloud-native % cd foundation 
leopoldsaublet@MacBook-Air-de-Leopold foundation % terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # scaleway_domain_record.dns will be created
  + resource "scaleway_domain_record" "dns" {
      + data       = "0.0.0.0"
      + dns_zone   = "polytech-dijon.kiowy.net"
      + fqdn       = (known after apply)
      + id         = (known after apply)
      + name       = "calculatrice-victor-leopold"
      + priority   = (known after apply)
      + project_id = (known after apply)
      + root_zone  = (known after apply)
      + ttl        = 300
      + type       = "A"
    }

  # scaleway_k8s_cluster.cluster will be created
  + resource "scaleway_k8s_cluster" "cluster" {
      + apiserver_url               = (known after apply)
      + cni                         = "cilium"
      + created_at                  = (known after apply)
      + delete_additional_resources = true
      + id                          = (known after apply)
      + kubeconfig                  = (sensitive value)
      + name                        = "calculatrice-victor-leopold-cluster"
      + organization_id             = (known after apply)
      + pod_cidr                    = (known after apply)
      + project_id                  = (known after apply)
      + service_cidr                = (known after apply)
      + service_dns_ip              = (known after apply)
      + status                      = (known after apply)
      + type                        = (known after apply)
      + updated_at                  = (known after apply)
      + upgrade_available           = (known after apply)
      + version                     = "1.27.4"
      + wildcard_dns                = (known after apply)

      + auto_upgrade (known after apply)

      + autoscaler_config (known after apply)

      + open_id_connect_config (known after apply)
    }

  # scaleway_lb.loadbalancer will be created
  + resource "scaleway_lb" "loadbalancer" {
      + external_private_networks = false
      + id                        = (known after apply)
      + ip_address                = (known after apply)
      + ip_id                     = (known after apply)
      + ip_ids                    = (known after apply)
      + ipv6_address              = (known after apply)
      + name                      = "calculatrice-lb"
      + organization_id           = (known after apply)
      + private_ips               = (known after apply)
      + project_id                = (known after apply)
      + region                    = (known after apply)
      + ssl_compatibility_level   = "ssl_compatibility_level_intermediate"
      + type                      = "LB-S"

      + private_network (known after apply)
    }

  # scaleway_rdb_instance.database will be created
  + resource "scaleway_rdb_instance" "database" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = false
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-15"
      + id                        = (known after apply)
      + is_ha_cluster             = false
      + name                      = "calculatrice-database"
      + node_type                 = "db-dev-s"
      + organization_id           = (known after apply)
      + project_id                = (known after apply)
      + read_replicas             = (known after apply)
      + settings                  = (known after apply)
      + upgradable_versions       = (known after apply)
      + user_name                 = (known after apply)
      + volume_size_in_gb         = (known after apply)
      + volume_type               = "lssd"

      + logs_policy (known after apply)

      + private_ip (known after apply)
    }

  # scaleway_registry_namespace.registry will be created
  + resource "scaleway_registry_namespace" "registry" {
      + endpoint        = (known after apply)
      + id              = (known after apply)
      + name            = "calculatrice-victor-leopold"
      + organization_id = (known after apply)
      + project_id      = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.



## Auteurs

Léopold SAUBLET \ Victor OLIVIER

