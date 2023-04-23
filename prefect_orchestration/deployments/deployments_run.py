'''
This script runs a Prefect deployment to extract stations from a given network 
by downloading web batch data and saving it locally.
The main() function runs the deployment using the run_deployment() function 
from the Prefect deployments module. 
The response from the deployment is then printed to the console.
'''
import argparse
import subprocess
from prefect.deployments import run_deployment

def main(args) -> None:
    stage = args.stage
    
    if stage == 'S1':
        print('Web -> GCS') 
        response = run_deployment("Flow extracting stations from a given network/Download web batch data and save it to GCS")
        print(response)
    
    elif stage == 'S2':
        print('Submitting Spark job') 
        subprocess.run("./gcloud_submit_job.sh",shell=True)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage data pipeline deployments")
    parser.add_argument('--stage', required=True, help='"S1" for web -> GCS, "S2" GCS -> BigQuery')
    
    args = parser.parse_args()
    main(args)