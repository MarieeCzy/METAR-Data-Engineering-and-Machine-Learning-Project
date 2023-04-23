gcloud dataproc jobs submit pyspark \
    --cluster=metar-dataproc-cluster \
    --region=europe-west1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://batch-metar-bucket-v2/code/pyspark_sql.py \
    -- \
        --input=gs://batch-metar-bucket-v2/data/PL__ASOS/*/* \
        --output=reports.PL_ASOS

#chmod +x submit_spark_job.sh
#./submit_spark_job.sh

