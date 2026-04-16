output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

output "gcs_bucket_name" {
  description = "Name of the GCS data lake bucket"
  value       = google_storage_bucket.data-lake.name
}

output "bq_dataset_id" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.dataset.dataset_id
}

output "region" {
  description = "GCP region"
  value       = var.region
}

output "location" {
  description = "GCP resource location"
  value       = var.location
}
