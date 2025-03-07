from airflow import DAG
from datetime import timedelta,datetime
import json
import requests
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.sensor.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

#load json config file
with open('/home/ubuntu/airflow/config_api.json','r') as config_file:
    api_host_key = json.load(config_file)

now=datetime.now()
dt_now_string=now.strftime("%d%m%Y%H%M%S")

#define the s3 bucket
s3_bucket='cleaned-data-zone-csv-bucket'

def extract_zillow_data(**kwargs):
      url=kwargs['url']
      headers=kwargs['headers']
      querystring = kwargs['querystring']
      dt_string = kwargs['date_string']

      response=requests.get(url,headers=headers,params=querystring)
      response_data=response.json()

      #specify the output file path
      output_file_path=f"/home/ubuntu/reponse_data_{dt_string}.json"
      file_str=f'response_data_{dt_string}.csv'

      
    # Write the JSON response to a file
      with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4)
    
      output_list=[output_file_path,file_str]


default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 3),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('Zillow_analytics_dag',
         default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:
    
        extract_zillow_data_var=PythonOperator(
              task_id='tsk_extract_zillow_data_var',
              python_callable=extract_zillow_data,
              op_kwargs={'url':'https://zillow56.p.rapidapi.com/search','querystring':{"location":"houston,tx"},'headers':api_host_key,'date_string':dt_now_string}
        )

        load_to_s3=BashOperator(
              task_id='tsk_load_to_s3',
              bash_command='aws s3 mv {{ti.xcom_pull("tsk_extract_zillow_data_var")[0]}} s3://endtoend-vizhi-bucket/',
        )

        is_file_in_s3_available=S3KeySensor(
              task_id='tsk_is_file_in_s3_available',
              bucket_key='{{ti.xcom_pull("tsk_extract_zillow_data_var")[1]}}',
              bucket_name=s3_bucket,
              aws_conn_id='aws_s3_conn',
              wildcard_match=False, 
              timeout=60,  # Optional: Timeout for the sensor (in seconds)
              poke_interval=5,  # Optional: Time interval between S3 checks (in seconds)
        )
        
        transfer_s3_to_redshift=S3ToRedshiftOperator(
             task_id="tsk_transfer_s3_to_redshift",
             aws_conn_id='aws_s3_conn',
             redshift_conn_id='conn_id_redshift',
             s3_bucket=s3_bucket,
             s3_key='{{ti.xcom_pull("tsk_extract_zillow_data_var")[1]}}',
             schema="PUBLIC",
             table="zillowdata",
             copy_options=["csv IGNOREHEADER 1"]
    )

        extract_zillow_data_var >> load_to_s3 >> is_file_in_s3_available >> transfer_s3_to_redshift
