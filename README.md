# Zillow Data Engineering ETL Pipeline
This project demonstrates how to build and automate an ETL pipeline using Python and Apache Airflow. The pipeline extracts real estate property data from the Zillow Rapid API, loads it into an Amazon S3 bucket, then triggers a series of AWS Lambda functions for transforming the data and converting it into a CSV file format. Finally, the data is loaded into Amazon Redshift for analytics, and Amazon QuickSight is used to visualize the data.

The entire project is carried out on the AWS Cloud Platform and utilizes Apache Airflow for orchestrating and scheduling the ETL pipeline.

## Overview
### High-Level Workflow:

Extract Data: Fetch real estate property data from the Zillow Rapid API.

Load to S3: The extracted data is uploaded to an Amazon S3 bucket.

Transformation via AWS Lambda: A Lambda function is triggered to transform the data and convert it into CSV format.

Monitor S3 with Apache Airflow: Using the S3KeySensor operator in Apache Airflow to monitor if the transformed data has been uploaded to the S3 bucket.

Load to Redshift: Once the data is available in S3, it is transferred to Amazon Redshift for analytics.

Visualize with Amazon QuickSight: Connect Amazon QuickSight to the Redshift cluster to visualize and analyze the Zillow data.

## Technologies Used:
Apache Airflow: For orchestrating and scheduling ETL tasks.

Amazon S3: For storing raw and transformed data.

AWS Lambda: For data transformation.

Amazon Redshift: For storing transformed data and enabling analytics.

Amazon QuickSight: For visualizing the Zillow data.

## Features:
1.Automated extraction of real estate property data using the Zillow Rapid API.

2.Data transformation into CSV format using AWS Lambda functions.

3.Orchestration and scheduling of tasks with Apache Airflow.

4.S3 monitoring with the S3KeySensor operator in Airflow.

5.Data loading into Amazon Redshift for analytics.

6.Visualization of the data with Amazon QuickSight.

## Prerequisites
AWS Account: To set up S3 buckets, Lambda functions, Redshift clusters, and QuickSight.

Apache Airflow: To orchestrate the ETL pipeline.

Python: Used for developing the transformation logic and setting up Airflow tasks.

Zillow API Key: You will need a RapidAPI key to access the Zillow API.
