resource "google_service_account" "service_account" {
  account_id   = var.account_id
  display_name = var.display_name
  description  = "${var.display_name} Service Account for ${var.project} project"
}

resource "google_project_iam_member" "account_roles" {
  project = var.project
  role    = var.role
  member  = "serviceAccount:${google_service_account.service_account.email}"
}
