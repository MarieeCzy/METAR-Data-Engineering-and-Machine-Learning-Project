'''
This module is responsible for uploading local parquet files to Google Cloud Storage 
using Prefect orchestration tool.
'''

import pathlib
from os import listdir
from prefect import task, flow
from prefect_gcp.cloud_storage import GcsBucket


@flow
def get_localfile_path() -> pathlib.Path:
    '''
    
    '''
    network_list = []
    parent_directory_path = str(pathlib.Path(__file__).parent.absolute())
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
                
                
@task
def load_from_path_to_gcs(parquet_path: pathlib.Path) -> None:
    '''
    
    '''
    gcs_block = GcsBucket.load("google-cloud-storage-bucket-block-metar")
    gcs_block.upload_from_path(from_path=parquet_path, to_path=parquet_path)

                
@flow
def local_to_gcs() -> None:
    get_localfile_path()

if __name__ == '__main__':
    local_to_gcs()