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
parser.add_argument('--temp_bucket', required=True)

args = parser.parse_args()

input = args.input
bq_output = args.bq_output
temp_bucket = args.temp_bucket


class SparkManager:
    def __init__(self,
                 temp_bucket) -> None:

        self.temp_bucket = temp_bucket
        self.spark_conf = self.spark_configuration()
        self.spark_ctx = self.spark_context()
        self.spark = self.spark_sesion_builder()

    def spark_configuration(self):
        conf = SparkConf()\
            .set("spark.sql.parquet.writeLegacyFormat", "true")\
            .set("spark.sql.files.ignoreCorruptFiles", "true")\
            .set("spark.sql.debug.maxToStringFields", 1000)\
            .set('temporaryGcsBucket', self.temp_bucket)

        return conf

    def spark_context(self):
        sc = SparkContext(conf=self.spark_conf)
        return sc

    def spark_sesion_builder(self):
        spark = SparkSession.builder \
            .appName('metar-project') \
            .config(conf=self.spark_ctx.getConf())\
            .getOrCreate()
        return spark


spark_manager = SparkManager(temp_bucket=temp_bucket)
spark = spark_manager.spark


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


class DataTransformationManager:
    def __init__(self,
                 schema: types.StructType,
                 spark: SparkSession,
                 temp_table_name: str,
                 sql_query,
                 bq_output) -> None:

        self.spark = spark
        self.schema = schema
        self.temp_table_name = temp_table_name
        self.sql_query = sql_query
        self.data_frame = self.data_frame_writer()
        self.data_frame_transformed = self.data_frame_transformations()
        self.pyspark_query = self.sql_query_maker()
        self.bq_output = bq_output

    def data_frame_writer(self):
        df = self.spark.read\
            .schema(schema=self.schema)\
            .parquet(input)
        return df

    def data_frame_transformations(self):
        df_transformed = self.data_frame\
            .withColumn('valid', to_timestamp(col('valid'), 'yyy-MM-dd HH:mm'))\
            .replace(0.0, 360.0, "drct") \
            .drop('p01i') \
            .withColumn("skyc1", when(self.data_frame["skyc1"].isin("FEW", "OVC", "SCT", "BKN", "NSC", "VV"), self.data_frame["skyc1"])
                        .otherwise(None))
        return df_transformed

    def sql_query_maker(self):
        self.data_frame_transformed \
            .registerTempTable(self.temp_table_name)

        query = self.spark.sql(self.sql_query)
        return query

    def bq_writer(self):
        self.pyspark_query.write.format('bigquery') \
            .option('table', self.bq_output + '_' + self.temp_table_name) \
            .mode("overwrite") \
            .save()


bq_tables_to_create = {
    "data_all":
    '''
    SELECT *,
    CONCAT(lat,", ", lon) AS GEOloc
    FROM data_all
    ''',

    "data_wxcodes":
    '''
    SELECT station, COUNT(*) AS sum, wxcodes 
    FROM data_wxcodes
    WHERE wxcodes IS NOT NULL
    GROUP BY station, wxcodes
    ORDER BY station, sum DESC    
    '''
}


def main(bq_tables_to_create):
    for key, values in bq_tables_to_create.items():

        temp_table_name = key
        query = values

        bq_table_create = DataTransformationManager(schema=schema,
                                                    spark=spark,
                                                    temp_table_name=temp_table_name,
                                                    sql_query=query,
                                                    bq_output=bq_output)
        bq_table_create.bq_writer()


if __name__ == '__main__':
    main(bq_tables_to_create)
