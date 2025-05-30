import boto3
import random

import json

from datetime import datetime

kinesis_client = boto3.client('kinesis', region_name='us-east-1')

def generate_warehouse_sensor_data():
    return {
        "sensor_type": "warehouse",
        "warehouse_id": f"WH-{random.randint(1,6)}",
        "temperature": 22.5,  # Example temperature in Celsius
        "humidity": 55.0,     # Example humidity in percentage
        "timestamp": datetime.now().isoformat()  # Example timestamp
    }


def generate_vehicle_sensor_data():
    return {
        "sensor_type": "vehicle",
        "vehicle_id": f"VH-{random.randint(1,6)}",
        "speed": round(random.uniform(30, 120)),         # Example speed in km/h
        "location": {
            "latitude": round(random.uniform(-90.0, 90.0), 6),
            "longitude": round(random.uniform(-180.0, 180.0), 6)
        },
        "timestamp": datetime.now().isoformat()  # Example timestamp
    }



def lambda_handler(event, context):
    if random.choice([True, False]):
        sensor_data = generate_warehouse_sensor_data()
    else:
        sensor_data = generate_vehicle_sensor_data()

    sensor_data_json = json.dumps(sensor_data)

    response = kinesis_client.put_record(
        StreamName='iot',
        Data=sensor_data_json,
        PartitionKey=str(random.randint(1, 1000))
    )


    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Sensor data sent to Kinesis',
            'data': sensor_data,
            "kinesis_response": response
        })
    }


