import os
from datetime import datetime

from airflow.decorators import dag, task

GCS_BUCKET  = os.environ.get("GCS_BUCKET_NAME")
GCP_PROJECT = os.environ.get("GCP_PROJECT_ID")
GCS_PREFIX  = os.environ.get("GCS_PREFIX")
BQ_DATASET  = os.environ.get("BQ_DATASET_ID")


@dag(
    dag_id="gcs_to_bigquery",
    description="Load parquet files from GCS into BigQuery",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["olympics", "bigquery"],
)
def gcs_to_bigquery():

    @task()
    def list_gcs_files() -> list[str]:
        from google.cloud import storage
        
        client = storage.Client(project=GCP_PROJECT)
        blobs = client.list_blobs(GCS_BUCKET, prefix=GCS_PREFIX)
        files = [b.name for b in blobs if b.name.endswith(".parquet")]
        
        if not files:
            raise RuntimeError(f"No parquet files found in gs://{GCS_BUCKET}/{GCS_PREFIX}")
        return files

    @task()
    def load_to_bigquery(blob_names: list[str]):
        from google.cloud import bigquery
        
        client = bigquery.Client(project=GCP_PROJECT)
        
        # Create dataset if needed
        dataset_ref = bigquery.DatasetReference(GCP_PROJECT, BQ_DATASET)
        try:
            client.get_dataset(dataset_ref)
        except Exception:
            client.create_dataset(bigquery.Dataset(dataset_ref))
        
        for blob_name in blob_names:
            filename = os.path.basename(blob_name).replace(".parquet", "").replace("-", "_")
            table_ref = f"{GCP_PROJECT}.{BQ_DATASET}.{filename}"
            gcs_uri = f"gs://{GCS_BUCKET}/{blob_name}"
            
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.PARQUET,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            )
            
            job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
            job.result()

    files = list_gcs_files()
    load_to_bigquery(files)


gcs_to_bigquery()
