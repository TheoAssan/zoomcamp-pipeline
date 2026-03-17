# 📌 Prerequisites

## ☁️ Google Cloud Setup Guide

This project uses **Google Cloud Platform (GCP)** for cloud storage and infrastructure provisioning (via Terraform).

Before running any Terraform configurations, ensure you have a GCP account and a properly configured service account.  

👉 Get started here: [Google Cloud Console](https://console.cloud.google.com/)

---

## Step 1: Create a GCP Project

1. Sign in to Google Cloud using your Google account.
2. Create a new project.
3. Note your **Project ID** — this will be required later for Terraform deployment.

---

## Step 2: Create a Service Account

1. Navigate to **IAM & Admin → Service Accounts**.
2. Create a new service account for your project.
3. Grant it the **Viewer** role (initial setup).
4. Generate and download the service account key file (`.json`).

> **Note:**  
> Copy the contents of the downloaded key file into a file named `keys.json` inside your Terraform directory.

---

## Step 3: Configure Permissions (Programmatic Access)

1. Go to **IAM & Admin → IAM**.
2. Locate your service account and click the **Edit** (pencil) icon.
3. Add the following roles:  
   - **Storage Admin**  
   - **Storage Object Admin**  
   - **BigQuery Admin**

---

## Step 4: Enable Required APIs

Enable the following APIs for your project:  
- **IAM API**  
- **IAM Credentials API**

You can enable them via: **APIs & Services → Library** in the GCP Console.