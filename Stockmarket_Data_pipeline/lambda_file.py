import json
import boto3
import base64
from decimal import Decimal

# Initialize AWS Clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

# IMPORTANT: Replace with your actual table and bucket names
DYNAMO_TABLE = "stock-market-data"
S3_BUCKET = "stock-market-raw-data-yourinitials-date"

table = dynamodb.Table(DYNAMO_TABLE)

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            # Decode base64 Kinesis data
            raw_data = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
            payload = json.loads(raw_data)
            print(f"Processing record: {payload}")

            # Store raw data in S3
            try:
                s3_key = f"raw-data/{payload['symbol']}/{payload['timestamp'].replace(':', '-')}.json"
                s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=s3_key,
                    Body=json.dumps(payload),
                    ContentType='application/json'
                )
            except Exception as s3_error:
                print(f"Failed to save raw data to S3: {s3_error}")

            # Compute stock metrics and structure for DynamoDB
            price_change = payload["price"] - payload["previous_close"]
            price_change_percent = (price_change / payload["previous_close"]) * 100
            is_anomaly = "Yes" if abs(price_change_percent) > 5 else "No"
            
            processed_data = {
                "symbol": payload["symbol"],
                "timestamp": payload["timestamp"],
                "open": Decimal(str(payload["open"])),
                "high": Decimal(str(payload["high"])),
                "low": Decimal(str(payload["low"])),
                "price": Decimal(str(payload["price"])),
                "volume": int(payload["volume"]),
                "anomaly": is_anomaly
            }

            # Store in DynamoDB
            table.put_item(Item=processed_data)
            print(f"Stored processed data in DynamoDB.")

        except Exception as e:
            print(f"Error processing record: {e}")

    return {"statusCode": 200, "body": "Processing Complete"}
    
