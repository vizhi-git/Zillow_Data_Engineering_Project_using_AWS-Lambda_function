import boto3
import json

s3_client=boto3.client('s3')

def lambda_handler(event,context):
    source_bucket=event['Records'][0]['s3']['bucket']['name']
    object_key=event['Records'][0]['s3']['object']['key']

    target_bucket='copy_of_raw_json_bucket'
    copy_source={'Bucket':source_bucket,'Key':object_key}

    s3_client.copy_object(Bucket=target_bucket,Key=object_key,CopySource=copy_source)
    return{
        'statusCode':200,
        'body':json.dumps('Copy completed successfullt')
    }
