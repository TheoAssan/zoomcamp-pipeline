from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from google.cloud import storage
import requests
from datetime import datetime

# ==========================
# CHANGE THESE VARIABLES
# ==========================
GCS_BUCKET = "your-bucket-name"             # <-- Replace with your GCS bucket name
BIGQUERY_DATASET = "reddit_dataset"         # <-- Replace with your BigQuery dataset name
BIGQUERY_TABLE = "reddit_table"             # <-- Replace with your BigQuery table name
GCS_FILE_NAME = "data.csv"                  # <-- Replace with the desired file name in GCS
URL = "https://example.com/data.csv"        # <-- Replace with the URL of your CSV file
# ==========================

def stream_file_to_gcs():
    """Download file from URL and stream directly to GCS"""
    client = storage.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(GCS_FILE_NAME)

    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        blob.upload_from_file(r.raw, rewind=True)

with DAG(
    dag_id="gcs_to_bigquery_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["gcp", "stream", "example"]
) as dag:

    # Step 1: Stream file to GCS
    upload_to_gcs = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=stream_file_to_gcs
    )

    # Step 2: Create BigQuery dataset if it doesn't exist
    create_bq_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_bigquery_dataset",
        dataset_id=BIGQUERY_DATASET,
        location="US",                      # <-- Change location if needed
        gcp_conn_id="google_cloud_default",
    )

    # Step 3: Load CSV from GCS to BigQuery
    load_to_bq = GCSToBigQueryOperator(
        task_id="load_csv_to_bigquery",
        bucket=GCS_BUCKET,
        source_objects=[GCS_FILE_NAME],
        destination_project_dataset_table=f"{BIGQUERY_DATASET}.{BIGQUERY_TABLE}",
        source_format="CSV",
        write_disposition="WRITE_TRUNCATE",  # <-- Use WRITE_APPEND if you want to append instead of overwrite
        skip_leading_rows=1,                  # <-- Skip header row
        autodetect=True,                      # <-- Auto-detect schema
        gcp_conn_id="google_cloud_default",
    )

    # Task dependencies
    upload_to_gcs >> create_bq_dataset >> load_to_bq