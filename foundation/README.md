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

## Validation (local)

Commandes exécutées :
```bash
terraform fmt
terraform validate
terraform plan
```

Résumé du plan (extrait) :
- Création de 2 DNS (dev/prod)
- Création d'un cluster Kubernetes
- Création de 2 IP Load Balancer (dev/prod)
- Création de 2 bases PostgreSQL (dev/prod)
- Création du namespace Registry

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

## Resultats obtenus
```bash
leopoldsaublet@MacBook-Air-de-Leopold foundation % terraform fmt
leopoldsaublet@MacBook-Air-de-Leopold foundation % terraform validate
Success! The configuration is valid.

leopoldsaublet@MacBook-Air-de-Leopold foundation % terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # scaleway_domain_record.dns_dev will be created
  + resource "scaleway_domain_record" "dns_dev" {
      + data       = (known after apply)
      + dns_zone   = "polytech-dijon.kiowy.net"
      + fqdn       = (known after apply)
      + id         = (known after apply)
      + name       = "calculatrice-dev-victor-leopold"
      + priority   = (known after apply)
      + project_id = (known after apply)
      + root_zone  = (known after apply)
      + ttl        = 3600
      + type       = "A"
    }

  # scaleway_domain_record.dns_prod will be created
  + resource "scaleway_domain_record" "dns_prod" {
      + data       = (known after apply)
      + dns_zone   = "polytech-dijon.kiowy.net"
      + fqdn       = (known after apply)
      + id         = (known after apply)
      + name       = "calculatrice-victor-leopold"
      + priority   = (known after apply)
      + project_id = (known after apply)
      + root_zone  = (known after apply)
      + ttl        = 3600
      + type       = "A"
    }

  # scaleway_k8s_cluster.cluster will be created
  + resource "scaleway_k8s_cluster" "cluster" {
      + apiserver_url               = (known after apply)
      + cni                         = "cilium"
      + created_at                  = (known after apply)
      + delete_additional_resources = false
      + id                          = (known after apply)
      + kubeconfig                  = (sensitive value)
      + name                        = "calculatrice-victor-leopold"
      + organization_id             = (known after apply)
      + pod_cidr                    = (known after apply)
      + project_id                  = (known after apply)
      + service_cidr                = (known after apply)
      + service_dns_ip              = (known after apply)
      + status                      = (known after apply)
      + type                        = (known after apply)
      + updated_at                  = (known after apply)
      + upgrade_available           = (known after apply)
      + version                     = "1.27.0"
      + wildcard_dns                = (known after apply)

      + auto_upgrade (known after apply)

      + autoscaler_config (known after apply)

      + open_id_connect_config (known after apply)
    }

  # scaleway_lb_ip.lb_dev will be created
  + resource "scaleway_lb_ip" "lb_dev" {
      + id              = (known after apply)
      + ip_address      = (known after apply)
      + is_ipv6         = false
      + lb_id           = (known after apply)
      + organization_id = (known after apply)
      + project_id      = (known after apply)
      + region          = (known after apply)
      + reverse         = (known after apply)
    }

  # scaleway_lb_ip.lb_prod will be created
  + resource "scaleway_lb_ip" "lb_prod" {
      + id              = (known after apply)
      + ip_address      = (known after apply)
      + is_ipv6         = false
      + lb_id           = (known after apply)
      + organization_id = (known after apply)
      + project_id      = (known after apply)
      + region          = (known after apply)
      + reverse         = (known after apply)
    }

  # scaleway_rdb_instance.db_dev will be created
  + resource "scaleway_rdb_instance" "db_dev" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = false
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-13"
      + id                        = (known after apply)
      + is_ha_cluster             = false
      + name                      = "calculatrice-dev-victor-leopold"
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

  # scaleway_rdb_instance.db_prod will be created
  + resource "scaleway_rdb_instance" "db_prod" {
      + backup_same_region        = (known after apply)
      + backup_schedule_frequency = (known after apply)
      + backup_schedule_retention = (known after apply)
      + certificate               = (known after apply)
      + disable_backup            = false
      + endpoint_ip               = (known after apply)
      + endpoint_port             = (known after apply)
      + engine                    = "PostgreSQL-13"
      + id                        = (known after apply)
      + is_ha_cluster             = false
      + name                      = "calculatrice-prod-victor-leopold"
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

Plan: 8 to add, 0 to change, 0 to destroy.

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
leopoldsaublet@MacBook-Air-de-Leopold foundation % 
```
