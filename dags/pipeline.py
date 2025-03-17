import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from include.function import upload_raw_data_to_bronze, process_bronze_to_silver, process_silver_to_gold
from datetime import datetime
from airflow.decorators import task, dag

@dag(dag_id="pipeline",
     description="pipeline_csv",
     start_date=datetime(2025,3,17),
     schedule="* * * * *",
     catchup=False)

def pipeline():

    @task(task_id='bronze')
    def task_bronze():
        upload_raw_data_to_bronze('raw_data.csv')
    
    @task(task_id='silver')
    def task_silver():
        process_bronze_to_silver('dados_bronze.csv')
    
    @task(task_id='gold')
    def task_gold():
        process_silver_to_gold('dados_silver.csv')

    t1 = task_bronze()
    t2 = task_silver()
    t3 = task_gold()

    t1 >> t2 >> t3

pipeline()
    