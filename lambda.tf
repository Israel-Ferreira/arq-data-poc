data "aws_iam_role" "lambda-iam-role" {
    name = "sensor-iot-role"
}


data "archive_file" "zip-lambda-producer" {
    type        = "zip"
    source_dir  = "${path.module}/producer-sensor"
    output_path = "${path.module}/producer-sensor.zip"
}

resource "aws_lambda_function" "sensor_iot_producer" {
    function_name = "sensor-iot-producer"
    role          = data.aws_iam_role.lambda-iam-role.arn
    handler       = "sensor_iot.lambda_handler"
    runtime       = "python3.11"

    source_code_hash = data.archive_file.zip-lambda-producer.output_base64sha256
    filename         = data.archive_file.zip-lambda-producer.output_path

    environment {
        variables = {
            STREAM_NAME = aws_kinesis_stream.broker-kinesis.name
        }
    }

    tags = {
        Name = "sensor-iot-producer"
    }

    depends_on = [ aws_kinesis_stream.broker-kinesis, data.aws_iam_role.lambda-iam-role ]
}
