import boto3
import base64


import json

from datetime import datetime

s3_client = boto3.client('s3', region_name='us-east-1')

BUCKET_NAME = "globalsupplydata-bucket"

def lambda_handler(event, context):
    for record in event['Records']:
        # Get the S3 bucket and object key from the Kinesis record
        kinesis_data = record['kinesis']['data']
        decoded_data = base64.b64decode(kinesis_data).decode('utf-8')

        try:
            payload = json.loads(decoded_data)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from Kinesis data: {decoded_data}")
            continue
        

        current_date = datetime.utcnow().strftime('%Y/%m/%d')

        file_name = f"iot_data/{current_date}/sensor_data_{datetime.utcnow().strftime('%H%M%S')}.json"

        file_content = json.dumps(payload, indent=4)

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content
        )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Sensor data processed and stored in S3',
        })
    }
       