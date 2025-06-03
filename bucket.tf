resource "aws_s3_bucket" "data_bucket" {
    bucket = "globalsupplydata-bucket"
}


resource "aws_s3_object" "create-parquet-data" {
    bucket = aws_s3_bucket.data_bucket.bucket
    key    = "iot_parquet/"
}