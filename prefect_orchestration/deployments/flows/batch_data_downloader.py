'''
This module provides functionality to download weather data from specified networks and stations
and save it locally in Parquet format.

The downloaded data is saved in the data directory, with a subdirectory 
for each network and station containing a Parquet file with the name of the station:

/data/<network_name>/<station_name>/<station_name>.parquet
'''

import os
from . import config
import datetime
import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect.tasks import task_input_hash

#https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?
#station=EPKK&data=all&year1=2023&month1=1&day1=1&year2=2023&month2=3&day2=26&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=null&trace=T&direct=no&report_type=3&report_type=4
#France Hungary Poland Germany Spain Greece Italy  Austria United Kingdom


NETWORKS_SERVICE="https://mesonet.agron.iastate.edu/sites/networks.php?"
STATION_SERVICE="https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
FLOWS_ABSOLUTE_PATH=config.flows_absolute_path

stations_list = []

start_date = datetime.datetime(
    config.start_year,
    config.start_month,
    config.start_day
    )

#current date and time
end_date = datetime.datetime.now()

@task(retries=3,
      retry_delay_seconds=60,
      cache_key_fn=task_input_hash,
      cache_expiration=datetime.timedelta(minutes=1),
      task_run_name="Getting stations for {network_name} network")
def get_stations_form_network(network_name: str) -> list[str]: 
    '''
    Gets a list of weather stations from a specified network.

    Args:
        network_name (str): The network for which to retrieve weather stations.

    Returns:
        list[str]: A list of station IDs.

    Raises:
        HTTPError: If there is an error accessing the URL.

    Example:
        >>> get_stations_form_network('XY__ASOS')
        ['KAAA', 'KAAF', 'KABI', ...]
    '''
    
    network_url = f'{NETWORKS_SERVICE}network={network_name}&format=csv&nohtml=on'
    df = pd.read_csv(network_url)
    
    #"stid" - df column name including station name for each record -> see example in docstring
    stations_list = list(df.stid)
    return stations_list

@task(retries=3,
      retry_delay_seconds=60,
      cache_key_fn=task_input_hash,
      cache_expiration=datetime.timedelta(minutes=5),
      task_run_name="Reading data for {station_name} station")
def fetch_data_for_station(station_name: str) -> pd.DataFrame:
    '''
    Fetches weather data for a specified weather station.

    Args:
        station_name (str): The ID of the weather station for which to retrieve data.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the weather data.

    Raises:
        HTTPError: If there is an error accessing the URL.
    '''
    
    station_url = STATION_SERVICE + f"station={station_name}&data=all&"
    station_url += start_date.strftime("year1=%Y&month1=%m&day1=%d&")
    station_url += end_date.strftime("year2=%Y&month2=%m&day2=%d&")
    station_url += "tz=Etc%2FUTC&format=onlycomma&latlon=yes&elev=yes&missing=null&trace=T&direct=no&report_type=3&report_type=4"
    
    df = pd.read_csv(station_url, low_memory=False)
    return df

@task(task_run_name="Saving data for {station_name} station")
def write_local(
    df: pd.DataFrame, 
    network_name:str, 
    station_name: str
    ) -> Path:
    '''
    Writes a Pandas DataFrame to local disk in Parquet format, with gzip compression.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        network_name (str): The name of the network to which the station belongs.
        station_name (str): The name of the station for which the DataFrame contains data.

    Returns:
        Path: The path to the saved file.
    '''
    
    path = Path(f'{FLOWS_ABSOLUTE_PATH}/data/{network_name}/{station_name}/{station_name}.parquet')
    
    df.to_parquet(path, compression='gzip')
    print(f'{network_name} {station_name} - saved.')
    return path

        
@flow(name='Flow managing local data storage', 
      flow_run_name=f"Local data storage start date: {start_date.strftime('%d.%m.%Y')}, end date: {end_date.strftime('%d.%m.%Y')}",
      log_prints=True)
def station_data_writer(
    stations_list: list[str], 
    network_name: str
    ) -> None:
    '''
    Fetches weather data for each station in a list of stations and saves it locally.

    Args:
        stations_list (list[str]): A list of station IDs for which to retrieve data.
        network_name (str): The name of the network to which the stations belong.

    Returns:
        None
    '''
    
    for station_name in stations_list:
        
        try:
            os.mkdir(f'{FLOWS_ABSOLUTE_PATH}/data/{network_name}/{station_name}')
        except FileExistsError:
            pass
        
        df = fetch_data_for_station(station_name)
        write_local(df, network_name, station_name)

@flow(name='Flow extracting stations from a given network', log_prints=True)
def extract_stations_and_transfer_to_save(
    networks_list: list[str]=config.networks_list,
    
    ) -> None:
    '''
    Fetches weather data for multiple networks and saves it locally.
    
    Args:
        None

    Returns:
        None
    '''
    
    try:
        os.mkdir(f'{FLOWS_ABSOLUTE_PATH}/data')
    except FileExistsError:
        pass

    for network_name in networks_list:
        
        try:
            os.mkdir(f'{FLOWS_ABSOLUTE_PATH}/data/{network_name}')
        except FileExistsError:
            pass
                
        stations_list = get_stations_form_network(network_name)
        station_data_writer(stations_list, network_name)


if __name__ == "__main__":   
    extract_stations_and_transfer_to_save()
    