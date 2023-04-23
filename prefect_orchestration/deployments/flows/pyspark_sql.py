import argparse
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql.functions import col, to_timestamp
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

parser = argparse.ArgumentParser()

parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input = args.input
output = args.output

conf = SparkConf()\
    .set("spark.sql.parquet.writeLegacyFormat","true")\
    .set("spark.sql.files.ignoreCorruptFiles", "true")\
    .set("spark.sql.debug.maxToStringFields",1000)

sc = SparkContext(conf=conf)

spark = SparkSession.builder \
    .appName('metar-project') \
    .config(conf=sc.getConf())\
    .getOrCreate()
    
schema = types.StructType([
    types.StructField("station", types.StringType(), True),
    types.StructField("valid", types.StringType(), True),
    types.StructField("lon", types.DoubleType(), True),
    types.StructField("lat", types.DoubleType(), True),
    types.StructField("elevation", types.DoubleType(), True),
    types.StructField("tmpf", types.DoubleType(), True),
    types.StructField("dwpf", types.DoubleType(), True),
    types.StructField("relh", types.DoubleType(), True),
    types.StructField("drct", types.DoubleType(), True),
    types.StructField("sknt", types.DoubleType(), True),
    types.StructField("p01i", types.DoubleType(), True),
    types.StructField("alti", types.DoubleType(), True),
    types.StructField("mslp", types.DoubleType(), True),
    types.StructField("vsby", types.DoubleType(), True),
    types.StructField("gust", types.DoubleType(), True),
    types.StructField("skyc1", types.StringType(), True),
    types.StructField("skyc2", types.StringType(), True),
    types.StructField("skyc3", types.StringType(), True),
    types.StructField("skyc4", types.StringType(), True),
    types.StructField("skyl1", types.DoubleType(), True),
    types.StructField("skyl2", types.DoubleType(), True),
    types.StructField("skyl3", types.DoubleType(), True),
    types.StructField("skyl4", types.DoubleType(), True),
    types.StructField("wxcodes", types.StringType(), True),
    types.StructField("ice_accretion_1hr", types.DoubleType(), True),
    types.StructField("ice_accretion_3hr", types.DoubleType(), True),
    types.StructField("ice_accretion_6hr", types.DoubleType(), True),
    types.StructField("peak_wind_gust", types.DoubleType(), True),
    types.StructField("peak_wind_drct", types.DoubleType(), True),
    types.StructField("peak_wind_time", types.StringType(), True),
    types.StructField("feel", types.DoubleType(), True),
    types.StructField("metar", types.StringType(), True),
    types.StructField("snowdepth", types.DoubleType(), True)
])

df = spark.read\
    .schema(schema=schema)\
    .parquet(input)

df = df\
    .withColumn('valid', to_timestamp(col('valid'), 'yyy-MM-dd HH:mm'))\
    .drop('p01i')
        
df.registerTempTable('data')


sql_data = spark.sql('''
                 SELECT *
                 FROM data
                 ''')


#sql_data.coalesce(1) \
#    .write.parquet(output, mode='overwrite')

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = "dataproc-temp-europe-west1-382050721889-kfi3x12x"
spark.conf.set('temporaryGcsBucket', bucket)

sql_data.write.format('bigquery') \
    .option('table', output) \
    .save()
    
#gsutil cp pyspark_sql.py gs://batch-metar-bucket-v2/code/pyspark_sql.py