import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
import pyspark.sql.functions as F
import pyspark.sql.types as T

gluecontext = GlueContext(SparkContext.getOrCreate())
spark = gluecontext.spark_session
job = Job(gluecontext)
job.init('game_raw_to_curated', {})


# ===================================== Paths
RAW = "s3://game-growth-raw/"
CURATED = "s3://game-growth-curated/"

# ===================================== Reg Data
df_reg = spark.read \
    .option("delimiter", ";") \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(RAW + "reg_data/")
    
def_reg = df_reg.withColumn("reg_datetime", F.from_unixtime(F.col("reg_ts")))
print(f"Writing data into {CURATED}reg_data/")
def_reg.write.mode("overwrite") \
    .parquet(CURATED + "reg_data/")
    

    
# ===================================== Auth Data
df_auth = spark.read \
    .option("delimiter", ";") \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(RAW + "auth_data")
    
df_auth = df_auth.withColumn("auth_datetime", F.from_unixtime(F.col("auth_ts")))
print(f"Writing data into {CURATED}auth_data/")
df_auth.write.mode("overwrite") \
    .parquet(CURATED + "auth_data/")
    
# ===================================== AB test Data
# schema = T.StructType([
#         T.StructField("user_id", T.IntegerType(), True),
#         T.StructField("revenue", T.FloatType(), True),
#         T.StructField("testgroup", T.StringType(), True)
#     ])

    # .schema(schema) \

df_ab = spark.read \
    .option("delimiter", ";") \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(RAW + "ab_test/")
    
print(f"Writing data into {CURATED}ab_test/")
df_ab.write.mode("overwrite") \
    .parquet(CURATED + "ab_test/")
    
job.commit()