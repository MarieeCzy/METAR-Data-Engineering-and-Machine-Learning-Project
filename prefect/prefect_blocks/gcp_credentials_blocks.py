from prefect_gcp.credentials import GcpCredentials

gcs_credentials_block = GcpCredentials(
    service_account_file="../../.secrets/gcs_credentials_key.json"
)

gcs_credentials_block.save("gcs-credentials", overwrite=True)


