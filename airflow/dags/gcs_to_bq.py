"""
DAG — GCS → BigQuery
Loads every CSV uploaded by load_to_gcs (suffix -winter-26.csv) from the
GCS bucket into BigQuery. Each file becomes its own table in the dataset.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

from airflow.decorators import dag, task

log = logging.getLogger(__name__)

GCS_BUCKET       = "zc-olympicsdatalake-26"
GCP_PROJECT      = "de-zoomcamp26-487314"
GCS_PREFIX       = "olympics_data"
FILE_SUFFIX      = "winter-26"
BQ_DATASET       = "olympics_pipeline"
CREDENTIALS_PATH = "/opt/airflow/terraform/keys.json"


@dag(
    dag_id="gcs_to_bigquery",
    description="Load Milano Cortina 2026 CSVs from GCS into BigQuery",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["olympics", "bigquery"],
)
def gcs_to_bigquery():

    @task()
    def list_gcs_files() -> list[str]:
        """Return blob names under the prefix that match the winter-26 suffix."""
        from google.cloud import storage

        client = storage.Client(project=GCP_PROJECT)
        blobs = client.list_blobs(GCS_BUCKET, prefix=GCS_PREFIX)
        files = [
            b.name for b in blobs
            if b.name.endswith(f"-{FILE_SUFFIX}.csv")
        ]
        if not files:
            raise RuntimeError(
                f"No *-{FILE_SUFFIX}.csv files found under gs://{GCS_BUCKET}/{GCS_PREFIX}. "
                "Run the load_to_gcs DAG first."
            )
        log.info("Found %d file(s): %s", len(files), files)
        return files

    @task()
    def load_to_bigquery(blob_names: list[str]) -> None:
        """Load each GCS CSV into its own BigQuery table (auto-detect schema)."""
        from google.cloud import bigquery

        client = bigquery.Client(project=GCP_PROJECT)

        # Ensure the dataset exists
        dataset_ref = bigquery.DatasetReference(GCP_PROJECT, BQ_DATASET)
        try:
            client.get_dataset(dataset_ref)
        except Exception:
            client.create_dataset(bigquery.Dataset(dataset_ref))
            log.info("Created dataset %s.%s", GCP_PROJECT, BQ_DATASET)

        for blob_name in blob_names:
            # Derive table name from file stem, e.g. medals-winter-26 → medals_winter_26
            filename   = os.path.basename(blob_name)           # medals-winter-26.csv
            stem       = os.path.splitext(filename)[0]         # medals-winter-26
            table_name = stem.replace("-", "_")                # medals_winter_26
            table_ref  = f"{GCP_PROJECT}.{BQ_DATASET}.{table_name}"
            gcs_uri    = f"gs://{GCS_BUCKET}/{blob_name}"

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,       # first row is the header
                autodetect=True,           # infer column types automatically
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            )

            log.info("Loading %s → %s …", gcs_uri, table_ref)
            job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
            job.result()   # wait for completion

            table = client.get_table(table_ref)
            log.info("✓ %s — %d rows, %d columns", table_ref, table.num_rows, len(table.schema))

    files = list_gcs_files()
    load_to_bigquery(files)


gcs_to_bigquery()
