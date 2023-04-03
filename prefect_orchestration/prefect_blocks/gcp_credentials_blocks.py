from prefect_gcp.credentials import GcpCredentials

google_cloud_storage_credentials_block = GcpCredentials(
    service_account_file="../../.secrets/gcs_credentials_key.json"
)

google_cloud_storage_credentials_block.save("google-cloud-storage-credentials-metar", overwrite=True)


