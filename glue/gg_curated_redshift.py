import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from awsglue.dynamicframce import DynamicFrame

# ================================================ Job paramts to pass to : Airflow


# CURATED = args["CURATED_PATH"]          # e.g. s3://game-growth-curated/
CURATED = "s3://game-growth-curated/"
TEMP_DIR = "s3://game-growth-temp/"
REDSHIFT_CONN = "Redshift connection" 
DATABASE = "dev" 


# ================================================ Glue Job init
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init("gg_curated_to_redshift")


# ================================================ # Load and write dataset
def load_to_redshift(subpath: str, table_name: str):
    print(f"Processing {table_name}...")
    df = spark.read.parquet(f"{CURATED}{subpath}/")
    dyf = DynamicFrame.fromDF(df, glueContext, f"dy_{table_name}")

    schema_name = table_name.split(".")[0]
    create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame=DynamicFrame.fromDF(
            spark.createDataFrame([], df.schema), glueContext, "dummy"
        ),
        catalog_connection=REDSHIFT_CONN,
        connection_options={
            "preactions": create_schema_sql,  # Run SQL before load
            "dbtable": table_name,
            "database": DATABASE,
        },
        redshift_tmp_dir=TEMP_DIR,
    )

    # Write actual data
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame=dyf,
        catalog_connection=REDSHIFT_CONN,
        connection_options={
            "dbtable": table_name,
            "database": DATABASE,
            "preactions": f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM (SELECT 1) WHERE 1=0;"
        },
        redshift_tmp_dir=TEMP_DIR,
    )


# ================================================ Load dataset
load_to_redshift("reg_data", "staging.reg_data")
load_to_redshift("auth_data", "staging.auth_data")
load_to_redshift("ab_test", "staging.ab_test")

job.commit()

