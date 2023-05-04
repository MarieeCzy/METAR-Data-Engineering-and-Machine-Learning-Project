gcloud dataproc jobs submit pyspark \
    --cluster=metar-cluster \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://code-metar-bucket-2/code/pyspark_sql.py \
    -- \
        --input=gs://batch-metar-bucket-2/data/ES__ASOS/*/* \
        --bq_output=reports.ES__ASOS \
        --temp_bucket=dataproc-staging-bucket-metar-bucket-2

#chmod +x submit_spark_job.sh
#./submit_spark_job.sh

