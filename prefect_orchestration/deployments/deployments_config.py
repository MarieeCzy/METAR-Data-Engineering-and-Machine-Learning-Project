'''
This script builds and applies a Prefect deployments for 
downloading web batch data and saving it locally and to GCS.
'''

from flows.batch_data_downloader import extract_stations_and_transfer_to_save
from flows.local_to_gcs_parquet_loader import local_to_gcs
from prefect.deployments import Deployment

save_data_locally_deployment = Deployment.build_from_flow(
    flow=extract_stations_and_transfer_to_save,
    name="Download web batch data and save it locally",
    work_queue_name="default",
)

move_data_to_gcs_deployment = Deployment.build_from_flow(
    flow=local_to_gcs,
    name="Get path to file and save to GCS bucket",
    work_queue_name="default",
)

if __name__ == "__main__":
    save_data_locally_deployment.apply()
    move_data_to_gcs_deployment.apply()

