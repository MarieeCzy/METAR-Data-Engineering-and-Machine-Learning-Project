'''
This script builds and applies a Prefect deployment for 
downloading web batch data and saving it locally.
'''

from flows.batch_data_downloader import extract_stations_and_transfer_to_save
from prefect.deployments import Deployment

save_data_locally_deployment = Deployment.build_from_flow(
    flow=extract_stations_and_transfer_to_save,
    name="Download web batch data and save it locally",
    work_queue_name="default",
)

if __name__ == "__main__":
    save_data_locally_deployment.apply()
    

