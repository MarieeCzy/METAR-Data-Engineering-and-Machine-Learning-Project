# Weather Data Downloader and Local Storage

Module name: `batch_data_downloader.py`

This Python module allows users to download weather data from specified networks and stations and store it locally in Parquet format. The data is saved in the data directory, with a subdirectory for each network and station containing a Parquet file with the name of the station: 

`/data/<network_name>/<station_name>/<station_name>.parquet`

## Dependencies
```
os
datetime
pandas
pathlib
prefect
```

## Functions

This module includes the following functions:

`get_stations_form_network(network_name: str) -> list[str]`

This function retrieves a list of weather stations from a specified network.

`fetch_data_for_station(station_name: str) -> pd.DataFrame`

This function fetches weather data for a specified weather station.

`write_local(df: pd.DataFrame, network_name:str, station_name: str) -> Path`

This function writes a Pandas DataFrame to local disk in Parquet format, with gzip compression.

`station_data_writer(stations_list: list[str], network_name: str) -> None`

This function fetches weather data for each station in a list of stations and saves it locally.

## How to Use
1. Install the dependencies.

2. Configure the networks_list variable to select the desired networks. The code includes examples of available networks.

3. Set the start and end dates of the data to download with the start_date and end_date variables.

4.Run the station_data_writer function to download and store the data for the specified networks and stations.

## Note
This module uses the Iowa State University Mesonet service to download weather data.