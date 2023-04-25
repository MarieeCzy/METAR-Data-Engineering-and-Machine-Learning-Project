gcloud dataproc jobs submit pyspark \
    --cluster=metar-project-test \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://code/pyspark_sql.py \
    -- \
        --input=gs://batch-metar-bucket-1/data/ES__ASOS/*/* \
        --bq_output=reports.ES__ASOS \
        --temp_bucket=dataproc-temp-europe-west1-204246137998-xrofmh5o

#chmod +x submit_spark_job.sh
#./submit_spark_job.sh

