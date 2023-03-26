import os
import pandas as pd
from pathlib import Path
from prefect import flow, task

#https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?
#station=EPKK&data=all&year1=2023&month1=1&day1=1&year2=2023&month2=3&day2=26&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=null&trace=T&direct=no&report_type=3&report_type=4
#France Hungary Poland Germany Spain Greece Italy  Austria United Kingdom

@task(retries=3)
def get_stations_form_network(network: str) -> list[str]: 
    '''
    Gets a list of weather stations from a specified network.

    Args:
        network (str): The network for which to retrieve weather stations.

    Returns:
        list[str]: A list of station IDs.

    Raises:
        HTTPError: If there is an error accessing the URL.

    Example:
        >>> get_stations_form_network('XY__ASOS')
        ['KAAA', 'KAAF', 'KABI', ...]
    '''
    
    url = f'https://mesonet.agron.iastate.edu/sites/networks.php?network={network}&format=csv&nohtml=on'
    df = pd.read_csv(url)
    stations = list(df.stid)
    return stations

@task(retries=3)
def fetch_data(station: str) -> pd.DataFrame:
    '''
    Fetches weather data for a specified weather station.

    Args:
        station (str): The ID of the weather station for which to retrieve data.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the weather data.

    Raises:
        HTTPError: If there is an error accessing the URL.
    '''
    
    service_url = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?'
    url = f'{service_url}station={station}&data=all&year1=2021&month1=1&day1=1&year2=2023&month2=3&day2=26&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=null&trace=T&direct=no&report_type=3&report_type=4'
    df = pd.read_csv(url, low_memory=False)
    return df

@task
def write_local(df: pd.DataFrame, network_name:str, station_name: str) -> Path:
    '''
    Writes a Pandas DataFrame to local disk in Parquet format, with gzip compression.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        network_name (str): The name of the network to which the station belongs.
        station_name (str): The name of the station for which the DataFrame contains data.

    Returns:
        Path: The path to the saved file.
    '''
    
    path = Path(f'data/{network_name}/{station_name}/{station_name}.parquet')
    
    df.to_parquet(path, compression='gzip')
    print(f'{network_name} {station_name} - saved.')
    return path

        
@flow(log_prints=True)   
def data_writer(stations: list[str], network: str) -> None:
    '''
    Fetches weather data for each station in a list of stations and saves it locally.

    Args:
        stations (list[str]): A list of station IDs for which to retrieve data.
        network (str): The name of the network to which the stations belong.

    Returns:
        None
    '''
    
    for station in stations:
        
        try:
            os.mkdir(f'data/{network}/{station}')
        except FileExistsError:
            pass
        
        df = fetch_data(station)
        write_local(df, network_name=network, station_name=station)

@flow(log_prints=True)
def get_batch_data() -> None:
    '''
    Fetches weather data for multiple networks and saves it locally.
    
    Args:
        None

    Returns:
        None
    '''
    #networks = ['HU__ASOS','PL__ASOS']
    networks = ['FR__ASOS','HU__ASOS','PL__ASOS','DE__ASOS','ES__ASOS','GR__ASOS','IT__ASOS','AT__ASOS','GB__ASOS']
    
    for network in networks:
        
        try:
            os.mkdir(f'data/{network}')
        except FileExistsError:
            pass
        
        stations = get_stations_form_network(network=network)
        data_writer(stations, network)


if __name__ == "__main__":
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    
    get_batch_data()