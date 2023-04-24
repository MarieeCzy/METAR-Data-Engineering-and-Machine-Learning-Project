import argparse
import os.path
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql.functions import col, to_timestamp, concat, when
from pyspark.conf import SparkConf
from pyspark.context import SparkContext


parser = argparse.ArgumentParser()

parser.add_argument('--input', required=True)
parser.add_argument('--bq_output', required=True)

args = parser.parse_args()

input = args.input
bq_output = args.bq_output

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
    types.StructField("peak_wind_time", types.DoubleType(), True),
    types.StructField("feel", types.DoubleType(), True),
    types.StructField("metar", types.StringType(), True),
    types.StructField("snowdepth", types.DoubleType(), True)
])

df = spark.read\
    .schema(schema=schema)\
    .parquet(input)

df = df\
    .withColumn('valid', to_timestamp(col('valid'), 'yyy-MM-dd HH:mm'))\
    .replace(0.0, 360.0, "drct") \
    .drop('p01i') 

df = df\
    .withColumn("skyc1",when(df["skyc1"].isin("FEW", "OVC", "SCT", "BKN", "NSC", "VV"), df["skyc1"]) \
    .otherwise(None))
        
df.registerTempTable('data_all')
df.registerTempTable('data_wxcodes')
df.registerTempTable('data_stats')
df.registerTempTable('data_wind_drct')
df.registerTempTable('data_skyc1')


sql_data_all = spark.sql('''
                 SELECT *,
                 CONCAT(lat,", ", lon) AS GEOloc
                 FROM data_all
                 ''')

sql_wxcodes = spark.sql('''
                SELECT station, COUNT(*) AS sum, wxcodes 
                FROM data_wxcodes
                WHERE wxcodes IS NOT NULL
                GROUP BY station, wxcodes
                ORDER BY station, sum DESC
                ''')

sql_stats = spark.sql('''
                SELECT station, 
                ROUND(AVG(sknt),2) AS avr_wind_speed,
                ROUND(AVG((tmpf-32)/1.8),2) AS avg_air_temperature,
                ROUND(MAX((tmpf-32)/1.8),2) AS max_air_temperature,
                ROUND(MIN((tmpf-32)/1.8),2) AS min_air_temperature,
                ROUND(AVG(dwpf-32/1.8),2) AS avg_dew_point,
                ROUND(AVG(vsby),2) AS avg_visibility,
                ROUND(AVG(drct)) AS avg_wind_direction,
                ROUND(AVG(sknt),2) AS avg_wind_speed,
                ROUND(MAX(gust)) AS max_gust,
                ROUND(AVG(gust),2) AS avg_gust,
                CONCAT(lat,", ", lon) AS GEOloc
                FROM data_stats 
                GROUP BY station, GEOloc
                ''')

sql_wind_drct = spark.sql(f'''
                SELECT station ,COUNT(*) AS direction_recorded, drct 
                FROM data_wind_drct
                WHERE drct is not null
                GROUP BY station, drct
                ORDER BY station, direction_recorded DESC
                ''')

sql_skyc1 = spark.sql(f'''
                SELECT station, COUNT(*) AS sum, skyc1
                FROM data_skyc1
                WHERE skyc1 IS NOT NULL
                GROUP BY station, skyc1
                ORDER BY station, sum DESC
                ''')



#sql_data_all.coalesce(1) \
#    .write.parquet(gcs_output, mode='overwrite')

# Use the Cloud Storage bucket for temporary BigQuery export data used
# by the connector.
bucket = "dataproc-temp-europe-west1-382050721889-kfi3x12x"
spark.conf.set('temporaryGcsBucket', bucket)

sql_data_all.write.format('bigquery') \
    .option('table', bq_output) \
    .mode("overwrite") \
    .save()
    
sql_wxcodes.write.format('bigquery') \
    .option('table', bq_output+'_wxcodes_')\
    .mode("overwrite") \
    .save()
    
sql_stats.write.format('bigquery') \
    .option('table', bq_output+'_stats_')\
    .mode("overwrite") \
    .save()
    
sql_stats.write.format('bigquery') \
    .option('table', bq_output+'_wind_drct_')\
    .mode("overwrite") \
    .save()
    
sql_stats.write.format('bigquery') \
    .option('table', bq_output+'_skyc1_')\
    .mode("overwrite") \
    .save()
    

    
#gsutil cp pyspark_sql.py gs://batch-metar-bucket-v2/code/pyspark_sql.py