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

#Google Cloud Storage Bucket
resource "google_storage_bucket" "metar-de-project" {
  for_each = toset(var.buckets)
  name     = "${each.key}-metar-bucket-2"
  location = var.location
}


#BigQuery dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "reports"
  location   = var.location
}

#Dataproc cluster
resource "google_dataproc_cluster" "metar-cluster" {
  name                          = "metar-cluster"
  region                        = "europe-west2"
  graceful_decommission_timeout = "120s"

  cluster_config {
    staging_bucket = "dataproc-staging-bucket-metar-bucket-2"

    master_config {
      machine_type = "n1-standard-2"

      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 30
      }
    }

    worker_config {
      machine_type  = "n1-standard-2"
      num_instances = 2

      disk_config {
        boot_disk_size_gb = 30
        num_local_ssds    = 1
      }
    }
  }
}
