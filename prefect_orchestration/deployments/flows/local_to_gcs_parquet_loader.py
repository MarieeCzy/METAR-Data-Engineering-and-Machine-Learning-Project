'''
This module is responsible for uploading local parquet files to Google Cloud Storage 
using Prefect orchestration tool.
'''

import pathlib
from os import listdir
from prefect import task, flow
from prefect_gcp.cloud_storage import GcsBucket


@flow(flow_run_name="Extracting data from {parent_directory_path}")
def get_localfile_path(parent_directory_path: str) -> None:
    '''
    This function searches for a parquet file in the '/data' directory and its subdirectories,
    selects the file based on a predefined criterion, and uploads the file to a Google Cloud Storage (GCS)
    bucket using the load_from_path_to_gcs() function. If no such file is found, nothing is returned.
    
    Note:
        This function does not return any values. It simply uploads the selected parquet file to GCS.

    Raises:
        NotADirectoryError: If the given path is not a directory.
    '''
    
    network_list = []
    data_main = parent_directory_path + '/data'
    
    for network in listdir(data_main):
        if not network.startswith('.'):
            network_list.append(network)
            
            for network in network_list:
               data = data_main + f'/{network}'
               station = listdir(data)
               
               for s in station:
                try:
                    station_path = data + f'/{s}'
                    parquet_path = station_path + f'/{listdir(station_path)[0]}'
                    parquet_path = parquet_path.split('/flows/')[1]
                except NotADirectoryError:
                    pass
                
                load_from_path_to_gcs(pathlib.Path(parquet_path))
                
                
@task(log_prints=True)
def load_from_path_to_gcs(parquet_path: pathlib.Path) -> None:
    '''
     Uploads a parquet file to a Google Cloud Storage bucket.

    Parameters:
        parquet_path: A pathlib.Path object representing the path to the local parquet file to upload.
    
    Note:
        This function assumes that the GCS bucket already exists and that the name of the parquet file in the
        GCS bucket should be the same as its local name.

    '''
    gcs_block = GcsBucket.load("google-cloud-storage-bucket-block-metar")
    gcs_block.upload_from_path(from_path=parquet_path, to_path=parquet_path)

                
@flow (name='Load local parquet file to GCS bucket', log_prints=True)
def local_to_gcs() -> None:
    parent_directory_path = str(pathlib.Path(__file__).parent.absolute())
    get_localfile_path(parent_directory_path)

if __name__ == '__main__':
    local_to_gcs()