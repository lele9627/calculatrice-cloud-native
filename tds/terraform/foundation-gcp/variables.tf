variable "gcp_project" {
  type        = string
  description = "GCP project id"
}

variable "gcp_region" {
  type        = string
  description = "GCP region"
  default     = "europe-west1"
}

variable "gcp_zone" {
  type        = string
  description = "GCP zone"
  default     = "europe-west1-b"
}

variable "gcp_machine_type" {
  type        = string
  default     = "e2-medium"
}

variable "gcp_db_tier" {
  type        = string
  default     = "db-f1-micro"
}

variable "dns_zone" {
  type        = string
  description = "DNS zone ex: example.com."
  default     = "example.com."
}

variable "dns_record_name" {
  type        = string
  description = "Record name ex: calc.example.com."
  default     = "calc.example.com."
}

variable "vm_count" {
  type        = number
  description = "Nombre d'instances pour HA"
  default     = 2
}
