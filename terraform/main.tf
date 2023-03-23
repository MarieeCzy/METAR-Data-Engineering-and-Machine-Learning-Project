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
  project = "metar-de-project-alpha-381321"
}

module "service-account" {
  for_each     = toset(var.accounts)
  source       = "./modules/service-account"
  account_id   = "${each.value}-service-acc"
  display_name = "${each.value}-service-acc"
  project      = var.project
  role         = "roles/${each.value}.admin"
}



/*
terraform apply \
  -var="project=metar-de-project-alpha-381321" \
  -var='accounts=["bigquery", "storage"]'
*/




