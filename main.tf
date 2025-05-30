terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}


provider "aws" {
    region = "us-east-1"
}


# Criando um Broker no AWS Kinesis
resource "aws_kinesis_stream" "broker-kinesis" {
    name = "iot"


    tags = {
        Name = "iot-kinesis-stream"
    }

    shard_level_metrics = [
        "IncomingBytes",
        "OutgoingBytes"
    ]

    stream_mode_details {
      stream_mode = "ON_DEMAND"
    }
}

