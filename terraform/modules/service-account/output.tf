output "email" {
    description = "Service Account email"
    value = google_service_account.service_account.email
}

output "display_name" {
    description = "Service account name"
    value = google_service_account.service_account.display_name
}