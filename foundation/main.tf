terraform {
  required_version = ">= 0.13"

  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
}

provider "scaleway" {}

variable "project_name" {
  default = "calculatrice"
}

variable "binome_1" {
  default = "victor"
}

variable "binome_2" {
  default = "leopold"
}

variable "region" {
  default = "fr-par"
}

resource "scaleway_registry_namespace" "registry" {
  name   = "${var.project_name}-${var.binome_1}-${var.binome_2}"
  region = var.region
}

resource "scaleway_k8s_cluster" "cluster" {
  name                        = "${var.project_name}-${var.binome_1}-${var.binome_2}-cluster"
  region                      = var.region
  version                     = "1.27.4"
  cni                         = "cilium"
  delete_additional_resources = true
}

resource "scaleway_rdb_instance" "database" {
  name          = "${var.project_name}-database"
  engine        = "PostgreSQL-15"
  node_type     = "db-dev-s"
  region        = var.region
  is_ha_cluster = false
}

resource "scaleway_lb" "loadbalancer" {
  name = "${var.project_name}-lb"
  type = "LB-S"
}

resource "scaleway_domain_record" "dns" {
  dns_zone = "polytech-dijon.kiowy.net"
  name     = "calculatrice-${var.binome_1}-${var.binome_2}"
  type     = "A"
  ttl      = 300
  data     = "0.0.0.0"
}

