import sys
import json
sys.path.append('..')

#from deployments.flows import config
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.credentials import GcpCredentials

with open ('../deployments/flows/config.json', 'r') as f:
    config = json.load(f)

gcs_batch_bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("google-cloud-storage-credentials-metar"),
    #insert your GCS batch data bucket name in ../deployments/flows/config module
    bucket = config["batch_bucket_name"]
    )

gcs_batch_bucket_block.save("google-cloud-storage-bucket-block-metar", overwrite=True)
