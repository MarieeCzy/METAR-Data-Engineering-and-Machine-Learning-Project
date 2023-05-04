![Progress](https://camo.githubusercontent.com/46884dbe2b094a29e9fa03bed9985b0710df347f39dad448fd0799138b109eea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374617475732d576f726b5f696e5f70726f67726573732d79656c6c6f77)
![Stage1](https://img.shields.io/badge/Phase1-completed-green)

<h1 align="center">🌦️ METAR Data Engineering and Machine Learning Project 🛫</h1>

<p align="center">
  <a href="#technologies">Technologies</a> •
  <a href="#about-the-project">About the project</a> •
  <a href="#conceptual-architecture">Conceptual architecture</a> •
  <a href="#👉-phase-1">Phase 1</a> •
  <a href="#👉-phase-2">Phase 2</a> •
  <a href="#👉-phase-3-final-stage">Phase 3 - Final Stage</a> •
  <a href="#data-source">Data source</a> •
  <a href="#📊-looker-report">Looker report</a> •
  <a href="#🛠️-setup">Setup</a> 
</p>

---

## Technologies

 ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
 ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
 ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)

- [Dataproc](https://cloud.google.com/dataproc)
- [Apache Spark](https://spark.apache.org/)
- [PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Streamlit](https://streamlit.io/)

---

## About the project

An educational project to build an end-to-end pipline for near real-time and batch processing of data further used for visualisation 👀 and a machine learning model 🧠.

The project is designed to enable the preparation of an analytical summary of the variability of METAR weather reports over the years for airports of European countries. 

Read more about METAR here ➡️ [METAR](https://www.dronepilotgroundschool.com/reading-aviation-routine-weather-metar-report/)

In addition, the aim is to prepare a web application using the Streamlit library and machine learning algorithms to predict the trend of change of upcoming METAR reports.

---

## Conceptual architecture

![view1][Conceptual]

---

The project is divided into 3 phases according to the attached diagrams:

## 👉 Phase 1

Retrieval of archive data from source. Initial transformation.
Transfer of data to Data Lake - Google Cloud Storage. Transfer of data to Data Warehouse. Transformations using PySpark on Dataproc cluster. Visualisation of aggregated data on an interactive dashboard in Looker.

![view2][Milestone_1_platform]

---

## 👉 Phase 2

Preparing the environment for near-real-time data retrieval. 
Transformations of archived and live data using PySpark, preparation of data for machine learning model. 
Training and tuning stage of the model.

![view3][Milestone_2_platform]

---

## 👉 Phase 3 - Final stage 🥳

Collection of analytical reports for historical data, preparation of web dashboard with the ability to display the prediction of the nearest METAR report for a given airport and the likely trend of change.

![view4][Final_platform]

---

## Data source

💿 [IOWA STATE UNIVERSITY ASOS-AWOS-METAR Data](https://mesonet.agron.iastate.edu/request/download.phtml?network=PL__ASOS)

---

## 📊 Looker report

The report generated in Looker provides averages of METAR data, broken down by temperature, winds, directions, and weather phenomena, with accompanying charts. The data was scraped via URL and stored in raw form in Cloud Storage. PySpark and Dataproc were then used to prepare SQL tables with aggregation functions, which were saved in BigQuery. The Looker report directly utilizes these tables from BigQuery.

Additionally, it's possible to prepare a similar report for other networks. 
Below is an example for PL__ASOS. 

Check: [PL__ASOS](https://lookerstudio.google.com/reporting/ef5cab41-deeb-498e-95de-c29cf52a3fe6)

For more information, please refer to the <b>"Setup"</b> section.

![view5][Looker_report]




---

## 🛠️ Setup

1. Make sure you have Spark, PySpark, Google Cloud Platform SDK, Prefect and Terraform installed and configured.

2. Clone the repo

    ```shell
    $ git clone https://github.com/MarieeCzy/METAR-Data-Engineering-and-Machine-Learning-Project.git
    ```

3. Create a new python virtual environment.

    ```shell
    $ python -m venv venv
    ```

4. Activate the new virtual environment using source (Unix systems) or .\venv\Scripts\activate (Windows systems).

    ```shell
    $ source venv/bin/activate
    ```

5. Install packages from requirements.txt using pip. Make sure the requirements.txt file is in your current working directory.

    ```shell
    $ pip install -r requirements.txt
    ```
6. Create new project on the GCP platform, assign it as default and authorize:

    ```shell
    $ gcloud config set project <your_project_name>
    $ gcloud auth login
    ```

7. Configure variables for Terraform:
  
    6.1. In:
    
      `terraform.tfvars` 
     
     replace project name to the name of your project created within the Google Cloud Platform:

      `project     = <your_project_name>`

     go to terraform directory:

     `$ cd terraform/`

     initialize, plan and apply cloud resource creation:


     ```shell
     $terraform init
     $terraform plan
     $terraform apply
     ```

8. Configure the upload data, go to:
 `~/prefect_orchestration/deployments/flows/config.py`

    8.1. Complete the variables:

    - `network` select one network e.g. FR__ASOS,
    

    - `start_year`, `start_month`, `start_day` - complete the start date, make sure that the digits are not preceded by "0"
    

    - `batch_bucket_name` - enter the name of the created Google Cloud Storgage bucket

9. Set up Perfect, the task orchestration tool:

    9.1. Generate new KEY for storage service account:

    On Google Platform go to 
    
    IAM & Admin > Service Accounts, click on 
    
    `"storage-service-acc"` go to 
    
    KEYS and click on ADD KEY  > Create new key in JSON format.

    <b>Save it in a safe place, do not share it on GitHub or any other public place.</b>


    > In order not to change the code in the `gcp_credentials_blocks.py` block, create a .secrets directory:
     ~/METAR-Data-Engineering-and-Machine-Learning-Project/.secrets
    and put the downloaded key in it under the name:
    `gcp_credentials_key.json`


    9.2. Run Prefect server

    ```shell
    $ prefect orion start
    ```

    Go to: http://127.0.0.1:4200

    9.3. In `~/prefect_orchestration/prefect_blocks` run below commands in console to create Credentials and GCS Bucket blocks:

    ```shell
    $ python gcp_credentials_blocks.py
    $ python gcs_buckets_blocks.py 
    ```

    9.4. Configure Perfect Deployment:

    ```shell
    $ python prefect_orchestration/deployments/deployments_config.py
    ```

    9.5. Run Prefect Agent to enable deployment in "default" queue

    ```shell
    $ prefect agent start -q "default"
    ```

10. Start deployment stage 1 - S1: Downloading data and uploading to the Google Cloud Storage bucket

    Go to: `~/prefect_orchestration/deployments`
    and run in command line:

    ```shell
    $ python deployments_run.py --stage="S1"

    ```

    ☝️ You can observe the running deployment flow in Prefect UI :

    ![view6][Prefect_deployment]
    After the deployment is complete, you will find the data in the GCS bucket.

11. Configuration and commissioning stage 2 - S2: data transformation using PySpark and moving to BigQuery using Dataproc

    11.1. Go to `~/prefect_orchestration/deployments` in `gcloud_submit_job.sh` and check if given paths and names are correct:

    >As long as you haven't changed other names/settings other than those listed in this manual, everything should be fine.

    ```shell
    $ gcloud dataproc jobs submit pyspark \
    --cluster=metar-cluster \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://code-metar-bucket-2/code/pyspark_sql.py \
    -- \
        --input=gs://batch-metar-bucket-2/data/ES__ASOS/*/* \
        --bq_output=reports.ES__ASOS \
        --temp_bucket=dataproc-staging-bucket-metar-bucket-2
    ```


    11.2. Upload the `pyspark_sql.py` code to the bucket code.

    In `~/prefect_orchestration/deployments/flows`:

    ```shell
    $ gsutil cp pyspark_sql.py gs://code-metar-bucket-2/code/pyspark_sql.py
    ```
 
    11.3. Run deployment stage S2 GCS -> BigQuery on Dataproc cluster:

    ```shell
    $ python deployments_run.py --stage="S2"
    ```

    <b>If the Job was successful, you can go to BigQuery, where the generated data is located. Now you can copy my Looker report and replace the data sources, or prepare your own. 😎</b>



<!-- MARKDOWN LINKS & IMAGES -->
[Conceptual]: docs/images/Conceptual.jpg
[Final_platform]: docs/images/Final_platform.jpg
[Milestone_1_platform]: docs/images/Milestone_1_platform.jpg
[Milestone_2_platform]: docs/images/Milestone_2_platform.jpg
[Looker_report]: docs/report/Looker_report.jpg
[Prefect_deployment]: docs/images/prefect_deployment.jpg