'''
Configuration module 
'''
from os import environ
from pathlib import Path
import os

#path to root project directory
ROOT_DIR_PATH = Path(__file__)
DATA_RELATIVE_PATH = 'prefect_orchestration/deployments/flows/data'

#networks_list = ['FR__ASOS','HU__ASOS','PL__ASOS','DE__ASOS','ES__ASOS','GR__ASOS','IT__ASOS','AT__ASOS','GB__ASOS']
networks_list = ['HU__ASOS','PL__ASOS', 'IT__ASOS']

start_year = 2023
start_month = 1
start_day = 1


batch_bucket_name = "batch-metar-bucket-v1"

