# Terraform Configuration Guide

This guide walks you through setting up and running your Terraform project using Google Cloud Platform (GCP).
Ensure you have your gcp credentials and the necessary services enabled.

---

## 📦 Prerequisites

### Install Terraform

https://www.terraform.io/downloads

**Verify installation:**
```bash
terraform --version
```

---

## ⚙️ Step 1: Configure Project Variables

1. Copy your GCP service account key (JSON file) into this directory as `keys.json`.

2. Replace the `project_id` default in `variables.tf` with your actual GCP Project ID.

> **Note:** The `keys.json` file is git-ignored for security. Never commit credentials.

> **Tip:** You can keep the default values for `region`, `location`, `gcs_bucket_name`, and `credentials` provided in `variables.tf`. Adjust them if your setup differs.

---

## 🚀 Step 2: Initialize and Apply Terraform

 Run:

```bash
cd terraform
terraform init      # Initializes providers and modules
terraform plan      # Preview infrastructure changes
terraform apply     # Create the GCS bucket and BigQuery dataset
```

---

## 🔗 Step 3: Generate Environment File

After `terraform apply` completes, run the helper script to generate a `.env` file for Airflow:

```bash
bash generate_env.sh
```

This reads the Terraform outputs (`outputs.tf`) and writes `../airflow/.env` with all the GCP configuration values. The Airflow DAGs and docker-compose will pick them up automatically.

---

## ✨ Next Steps: Continue with Airflow Setup

 The next stage of the pipeline is setting up **Apache Airflow** to orchestrate data ingestion.

→ **[Proceed to Airflow Pipeline Setup](../airflow/README.md)**

This will guide you through:
- Building the Airflow Docker environment
- Running the data ingestion DAGs
- Validating data in BigQuery

