terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
}

module "service-account" {
  source       = "./modules/service-account"
  account_id   = var.service_account_id
  display_name = var.display_name
  project      = var.project_id
  role         = var.role
}





