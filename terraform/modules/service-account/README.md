# Terraform module description


This Terraform module creates a Google Cloud Service Account and assigns the specified role to it for the given project.

## Usage

```hcl
module "service_account" {
  source = "path/to/module"

  service_account_id = "example-sa"
  display_name       = "Example Service Account"
  project_id         = "example-project"
  role               = "roles/editor"
}
```

## Required variables

- `service_account_id`: The unique ID for the service account.
- `display_name`: The display name of the service account.
- `project_id`: The ID of the project where the service account will be created.
- `role`: The role to be assigned to the service account.

## Resources created
`google_service_account.service_account`: The Google Cloud Service Account.

`google_project_iam_member.account_roles`: The IAM binding between the service account and the specified role.
