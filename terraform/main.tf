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
  project = var.project
}

module "service-account" {
  for_each     = var.accounts
  source       = "./modules/service-account"
  account_id   = "${each.key}-service-acc"
  display_name = "${each.key}-service-acc"
  project      = var.project
  role         = each.value
}



/*
terraform apply \
  -var="project=metar-de-project-alpha-381321" \
  -var='accounts=["bigquery", "storage"]'
*/




