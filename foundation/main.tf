terraform {
  required_version = ">= 0.13"

  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
}

provider "scaleway" {
  region = var.region
}

####################
# VARIABLES
####################

variable "project_name" {
  type    = string
  default = "calculatrice"
}

variable "binome_1" {
  type    = string
  default = "victor"
}

variable "binome_2" {
  type    = string
  default = "leopold"
}

variable "region" {
  type    = string
  default = "fr-par"
}

####################
# LOCALS
####################

locals {
  binome = "${var.binome_1}-${var.binome_2}"
}

####################
# 1. REGISTRE
####################

resource "scaleway_registry_namespace" "registry" {
  name = "${var.project_name}-${local.binome}"
}

####################
# 2. CLUSTER KUBERNETES
####################

resource "scaleway_k8s_cluster" "cluster" {
  name    = "${var.project_name}-${local.binome}"
  version = "1.27.0"
  cni     = "cilium"

  delete_additional_resources = false
}

####################
# 3. BASE DE DONNÉES DEV
####################

resource "scaleway_rdb_instance" "db_dev" {
  name      = "${var.project_name}-dev-${local.binome}"
  engine    = "PostgreSQL-13"
  node_type = "db-dev-s"
}

####################
# 4. BASE DE DONNÉES PROD
####################

resource "scaleway_rdb_instance" "db_prod" {
  name      = "${var.project_name}-prod-${local.binome}"
  engine    = "PostgreSQL-13"
  node_type = "db-dev-s"
}

####################
# 5. LOADBALANCER DEV
####################

resource "scaleway_lb_ip" "lb_dev" {}

####################
# 6. LOADBALANCER PROD
####################

resource "scaleway_lb_ip" "lb_prod" {}

####################
# 7. DNS DEV
####################

resource "scaleway_domain_record" "dns_dev" {
  dns_zone = "polytech-dijon.kiowy.net"
  name     = "calculatrice-dev-${local.binome}"
  type     = "A"
  data     = scaleway_lb_ip.lb_dev.ip_address
}

####################
# 8. DNS PROD
####################

resource "scaleway_domain_record" "dns_prod" {
  dns_zone = "polytech-dijon.kiowy.net"
  name     = "calculatrice-${local.binome}"
  type     = "A"
  data     = scaleway_lb_ip.lb_prod.ip_address
}

