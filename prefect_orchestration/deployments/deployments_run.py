'''
This script runs a Prefect deployment to extract stations from a given network 
by downloading web batch data and saving it locally.
The main() function runs the deployment using the run_deployment() function 
from the Prefect deployments module. 
The response from the deployment is then printed to the console.
'''
import argparse
from prefect.deployments import run_deployment

def main(args) -> None:
    stage = args.stage
    
    if stage == 'S1':
        print('Web -> local') 
        response = run_deployment("Flow extracting stations from a given network/Download web batch data and save it locally")
        
    elif stage == 'S2':
        print('Local -> GCS') 
        response = run_deployment("Load local parquet file to GCS bucket/Get path to file and save to GCS bucket")
    
    print(response)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage data pipeline deployments")
    parser.add_argument('--stage', required=True, help='"S1" for WEB TO LOCAL, "S2" for LOCAL TO GCS')
    
    args = parser.parse_args()
    main(args)