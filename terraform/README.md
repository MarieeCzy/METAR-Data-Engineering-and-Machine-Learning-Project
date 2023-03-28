# Infrastructure as a Code with Terraform

This Terraform code creates Google Cloud Platform service accounts with specific roles for a given project and Google Cloud Storage buckets. It uses the hashicorp/google provider and a local backend.

## Requirements
Terraform version 1.0 or higher.

Access to a Google Cloud Platform project.

## Usage
1. Navigate to the project directory.

2. Set the required variables for the project and service accounts by modyfing a file named terraform.tfvars. Use the following format:

```hcl
project     = "metar-de-project-alpha-xyz"

accounts    = {
    bigquery    = "roles/bigquery.admin"
    storage     = "roles/storage.admin"
    main-viewer = "roles/viewer"
  }

buckets = ["batch", "streaming"]

location = "EU"
```

3. Run `terraform init` to initialize the backend and provider plugins.

4. Run `terraform apply` to create the service accounts with the roles specified in the role variable.

Note: If you only want to create specific service accounts, you can modify the accounts variable in `terraform.tfvars` accordingly.

## Variables

- `project`: The ID of the Google Cloud Platform project where the service accounts will be created.

- `accounts`: The map of strings representing the name of the service accounts and role to be created. These names will be appended with `-service-acc`.

- `role`: The role to be granted to the service accounts. The role must be in the format `roles/ROLE_NAME`.

- `buckets`: Any names that define the types of buckets to be created.

- `location`: GCS buckets location.

## Modules

The Terraform code uses a module located in the `./modules/service-account` directory to create the service accounts.

The module takes the following input variables:

- `account_id`: The ID of the service account.

- `display_name`: The display name of the service account.

- `project`: The ID of the Google Cloud Platform project where the service account will be created.

- `role`: The role to be granted to the service account.