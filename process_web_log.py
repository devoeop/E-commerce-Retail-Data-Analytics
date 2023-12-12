from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# Task arguments
default_args = {
    'owner': 'owner_name',
    'start_date': days_ago(0),
    'email': ['your_email@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    dag_id='process_web_log',
    description='DAG to process web server log daily',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    catchup=False,  # Don't process historical dates when the DAG is turned on
)

# Task 1: Extract Data
extract_data = BashOperator(
    task_id='extract_data',
    bash_command='cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt > /home/project/airflow/dags/capstone/extracted_data.txt',
    dag=dag,
)

# Task 2: Transform Data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='grep -v "198.46.149.143" /home/project/airflow/dags/capstone/extracted_data.txt > /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# Task 3: Load Data
load_data = BashOperator(
    task_id='load_data',
    bash_command='tar -cf weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# Define the task pipeline
extract_data >> transform_data >> load_data