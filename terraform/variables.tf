variable "role" {
  description = "The role that should be applied. Only one - required"
  type        = string
  default     = ""
}

variable "project" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

variable "account_id" {
  description = " The account id that is used to generate the service account email address and a stable unique id."
  type        = string
  default     = ""
}

variable "display_name" {
  description = "The display name for the service account. Can be updated without creating a new resource - optional"
  default     = ""
  type        = string
}

variable "accounts" {
  description = "Provide set of resources strings for creating roles, for example: 'bigquery'"
  type        = map(string)
}

variable "buckets" {
  description = "Provide buckets names for creating resources example: batch, realt-time"
  type        = list(string)
}

variable "location" {
  description = "(Required) The GCS location."
  type        = string
}
