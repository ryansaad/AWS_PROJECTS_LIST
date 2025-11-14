# Stockmarket_Data_pipeline
# Near Real-Time Stock Market Data Analytics Pipeline on AWS

This repository contains the code and complete instructions for building a near real-time, event-driven stock market data analytics pipeline using serverless services on AWS.
## ☁️ Project Overview

This project demonstrates a modern data engineering workflow designed to ingest, process, store, and analyze stock market data with minimal operational overhead. The architecture uses Amazon Kinesis for data ingestion, AWS Lambda for processing, Amazon S3 for long-term storage, Amazon DynamoDB for quick access, Amazon Athena for historical queries, and Amazon SNS for real-time trend alerts.

## ✨ Key Features

* **Real-Time Data Ingestion**: Streams stock data from external APIs using Amazon Kinesis Data Streams.
* **Serverless Processing**: Uses AWS Lambda to process incoming data, calculate key metrics, and detect anomalies.
* **Dual Storage Strategy**: Stores raw, immutable data in Amazon S3 for historical analysis and processed, structured data in Amazon DynamoDB for low-latency queries.
* **Ad-Hoc Querying**: Leverages Amazon Athena to run standard SQL queries directly on the raw data stored in S3.
* **Automated Trend Alerts**: Analyzes data streams for trend changes (e.g., moving average crossovers) and sends real-time alerts via email or SMS using Amazon SNS.


## 🛠️ Services & Technologies Used

* **Data Ingestion**: Amazon Kinesis Data Streams
* **Data Processing**: AWS Lambda
* **Real-Time Database**: Amazon DynamoDB
* **Data Lake / Historical Storage**: Amazon S3
* **Data Querying**: Amazon Athena, AWS Glue Data Catalog
* **Alerting**: Amazon SNS (Simple Notification Service)
* **Security**: IAM Roles & Policies
* **Data Source**: Python (`yfinance` library)

## 🚀 Getting Started

To build this pipeline yourself, you'll need an AWS account and a local Python environment with the AWS CLI configured.

For a complete, step-by-step guide, please see the instructions file:

## 🧹 Clean-Up

To avoid ongoing AWS charges, remember to delete all the resources created during this project. Detailed clean-up steps are provided at the end .
