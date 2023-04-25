import json
from prefect_gcp.credentials import GcpCredentials

with open('../../.secrets/gcp_credentials_key.json', 'r') as f:
    service_account_file = json.load(f)


google_cloud_storage_credentials_block = GcpCredentials(
    service_account_info=service_account_file
)

google_cloud_storage_credentials_block.save("google-cloud-storage-credentials-metar", overwrite=True)


