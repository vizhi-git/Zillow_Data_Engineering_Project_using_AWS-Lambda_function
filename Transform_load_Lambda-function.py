import boto3
import json
import pandas as Pd  
import logging

#Initialize logging
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger()

#Initialize s3 client
s3_client=boto3.client('s3')

def lambda_handler(event,context):
    try:
        source_bucket=event['Records'][0]['s3']['bucket']['name']
        object_key=event['Records'][0]['s3']['object']['key']

        target_bucket='cleaned_data_zone_csv_bucket'
        target_file_name=object_key[:-5]

        response=s3_client.get_object(Bucket=source_bucket,Key=object_key)
        data=response['Body'].read().decode('utf-8')
        logger.info("Data fetched from s3")

        data=json.loads(data)
        logger.info("Data parsed into JSON")

        f=[]
        for i in data["results"]:
          f.append(i)
        df=pd.DataFrame(f)

        selected_columns=['bathrooms','bedrooms','city','homestatus','homeType','livingarea','price','rentestimate','zipcode']

        df=df[selected_columns]
        logger.info("Columns selected successfully")

    #convert df to csv format
        csv_data=df.to_csv(index=False)

    #upload csv to s3
        bucket_name=target_bucket
        object_key=f"{target_file_name}.csv"
        s3_client.put_object(Bucket=bucket_name,Key=object_key,Body=csv_data)
        logger.info("CSV uploaded to target s3 bucket")

        return{
        'statusCode':200,
        'body':json.dumps('CSV conversion and S3 upload completed successfully')
    }
    except Exception as e:
        logger.error(f"Error occurred:{str(e)}")
        return{
            'statusCode':500,
            'body':json.dumps(f"Error occurred:{str(e)}")
        }
