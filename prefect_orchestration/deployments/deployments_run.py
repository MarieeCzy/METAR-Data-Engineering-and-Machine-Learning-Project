'''
This script runs a Prefect deployment to extract stations from a given network 
by downloading web batch data and saving it locally.
The main() function runs the deployment using the run_deployment() function 
from the Prefect deployments module. 
The response from the deployment is then printed to the console.
'''

from prefect.deployments import run_deployment

def main() -> None:
    response = run_deployment("Flow extracting stations from a given network/Download web batch data and save it locally")
    print(response)
    
if __name__ == "__main__":
    main()