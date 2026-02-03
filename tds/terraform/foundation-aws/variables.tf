variable "aws_region" {
  type    = string
  default = "eu-west-3"
}

variable "aws_az" {
  type    = string
  default = "eu-west-3a"
}

variable "aws_ami" {
  type        = string
  description = "AMI id"
}

variable "aws_instance_type" {
  type    = string
  default = "t3.micro"
}

variable "db_user" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "dns_zone" {
  type    = string
  default = "example.com"
}

variable "dns_record_name" {
  type    = string
  default = "calc"
}

variable "vm_count" {
  type    = number
  default = 2
}
