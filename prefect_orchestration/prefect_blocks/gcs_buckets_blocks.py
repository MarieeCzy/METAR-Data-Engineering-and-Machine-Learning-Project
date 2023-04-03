from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.credentials import GcpCredentials

gcs_batch_bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("google-cloud-storage-credentials-metar"),
    #insert your GCS batch data bucket name below
    bucket = "batch-metar-bucket" 
    )

gcs_batch_bucket_block.save("google-cloud-storage-bucket-block-metar", overwrite=True)