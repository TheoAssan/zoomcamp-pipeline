# Terraform Configuration Guide

This guide walks you through setting up and running your Terraform project using Google Cloud Platform (GCP).
Ensure you have your gcp credentials and the necessary services enabled.

---

## 📦 Prerequisites

### Install Terraform

**Linux / WSL:**

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

wget -O- https://apt.releases.hashicorp.com/gpg | \
  gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt-get update && sudo apt-get install -y terraform
```
Note: Codespaces have a different way of installing terraform. 


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

## 📁 File Structure

```
terraform/
├── main.tf           # GCS bucket + BigQuery dataset resources
├── variables.tf      # Input variables (project_id, region,etc.)
├── outputs.tf        # Exported values for downstream tools
├── generate_env.sh   # Script to generate .env from outputs
├── keys.json         # Your GCP service account key
└── README.MD         # This file
```