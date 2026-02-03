terraform {
  required_version = ">= 1.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "google_compute_network" "vpc" {
  name                    = "calc-vpc"
  auto_create_subnetworks = true
}

resource "google_compute_instance" "vm" {
  count        = var.vm_count
  name         = "calc-vm-${count.index}"
  machine_type = var.gcp_machine_type
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = google_compute_network.vpc.name
    access_config {}
  }

  tags = ["calc", "td"]
}

resource "google_sql_database_instance" "db" {
  name             = "calc-db"
  database_version = "POSTGRES_14"
  region           = var.gcp_region

  settings {
    tier = var.gcp_db_tier
  }
}

resource "google_dns_managed_zone" "zone" {
  name     = "calc-zone"
  dns_name = var.dns_zone
}

resource "google_dns_record_set" "dns" {
  name         = var.dns_record_name
  managed_zone = google_dns_managed_zone.zone.name
  type         = "A"
  ttl          = 300
  rrdatas      = [google_compute_instance.vm[0].network_interface[0].access_config[0].nat_ip]
}
