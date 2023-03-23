resource "google_service_account" "service_account" {
  account_id   = var.service_account_id
  display_name = var.display_name
  description  = "${var.display_name} Service Account for ${var.project_id} project"
}

resource "google_project_iam_member" "account_roles" {
  project = var.project_id
  role    = var.role
  member  = "seviceAccount:${google_service_account.service_account.email}"
}
