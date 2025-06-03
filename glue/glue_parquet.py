import sys

from awsglue.utils import getResolvedOptions
from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


datasource = glueContext.create_dynamic_frame.from_catalog(
    database="globalsupply-iot-data",
    table_name="iot_data",
)

df = datasource.toDF()

output_path = "s3://globalsupplydata-bucket/iot_parquet/"
df.write.mode("overwrite").partitionBy("partition_0", "partition_1", "partition_2").parquet(output_path)

job.commit()
