resource "aws_glue_catalog_database" "globalsupply-iot-data" {
  name = "globalsupply-iot-data"
}

data "aws_iam_role" "globalsupply-iot-crawler-role" {
    name = "AWSGlueServiceRole-GlobalSupply"
}


resource "aws_glue_crawler" "globalsupply-iot-crawler" {
  name          = "globalsupply-iot-crawler"
  role          = data.aws_iam_role.globalsupply-iot-crawler-role.arn
  database_name = aws_glue_catalog_database.globalsupply-iot-data.name

  s3_target {
    path = "s3://${aws_s3_bucket.data_bucket.bucket}/iot_data/"
  }

  configuration = jsonencode({
    Version = 1
    Grouping = {
      TableGroupingPolicy = "CombineCompatibleSchemas"
    }
  })


  tags = {
    Name = "globalsupply-iot-crawler"
  }
  
}