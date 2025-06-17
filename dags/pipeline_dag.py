from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys, os, yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'etl'))

with open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml')) as f:
    cfg = yaml.safe_load(f)

default_args = {
    'owner': 'ivan_ivanov',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'breast_cancer_pipeline',
    default_args=default_args,
    description='ML pipeline with Airflow and cloud logic',
    schedule_interval=None,
    start_date=datetime(2025,6,17),
    catchup=False
) as dag:

    task_load = PythonOperator(task_id='load_data', python_callable=lambda: __import__('load_data').load_data_task(cfg))
    task_pre = PythonOperator(task_id='preprocess', python_callable=lambda: __import__('preprocess').preprocess_task(cfg))
    task_train = PythonOperator(task_id='train_model', python_callable=lambda: __import__('train_model').train_task(cfg))
    task_eval = PythonOperator(task_id='evaluate', python_callable=lambda: __import__('evaluate').evaluate_task(cfg))
    task_save = PythonOperator(task_id='save_artifacts', python_callable=lambda: __import__('save_artifacts').save_task(cfg))

    task_load >> task_pre >> task_train >> task_eval >> task_save