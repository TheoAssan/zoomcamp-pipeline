variable "bq_dataset_id" {
  description = "Name of the Bigquery Dataset"
  default     = "olympics_pipeline_2"
}

variable "project_id" {
  description = "GCP Project ID"
  # default     = "xxx-xxx-xxx-xxx" # replace with your actual project id from GCP
}

variable "credentials" {
  description = "credentials for gcp service account"
  default     = "keys.json" # this file must be created and placed in the terraform directory
}

variable "region" {
  description = "storage bucket region"
  default     = "europe-west2" # you can adjust based on your location
}

variable "gcs_bucket_name" {
  description = "Name of the storage bucket"
  default     = "zc-olympicsdatalake-26_2"
}

variable "location" {
    description = "resource location"
    default = "EU" # you can adjust based on your location
}