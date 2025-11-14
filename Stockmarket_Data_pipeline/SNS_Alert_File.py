import boto3
import json
import decimal
from datetime import datetime, timedelta

# AWS Clients
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# IMPORTANT: Replace with your actual table name and SNS topic ARN
TABLE_NAME = "stock-market-data"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:Stock_Trend_Alerts" # Example ARN

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            symbol = new_image['symbol']['S']
            price = decimal.Decimal(new_image['price']['N'])
            
            # Simple Trend Logic: Send alert if price > a certain value
            # This is a basic example; a real-world scenario would use moving averages.
            if price > 200: # Example threshold
                message = f"Stock Alert for {symbol}! Price has exceeded ${price}."
                try:
                    sns.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Message=message,
                        Subject=f"Stock Price Alert: {symbol}"
                    )
                    print(f"Published SNS message: {message}")
                except Exception as e:
                    print(f"Failed to publish SNS message: {e}")

    return {"statusCode": 200, "body": "Trend analysis complete"}
