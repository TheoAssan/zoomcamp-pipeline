# Milano-Cortina 2026 Winter Olympics Pipeline — Makefile
# Run targets in order: terraform → generate-env → airflow
# dbt is run separately via dbt Cloud (see dbt/README.md)

.PHONY: help terraform-init terraform-plan terraform-apply terraform-destroy \
        generate-env airflow-build airflow-up airflow-down airflow-reset airflow-logs

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "} {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Terraform ───────────────────────────────────────────────────────

terraform-init: ## Initialize Terraform providers
	cd terraform && terraform init

terraform-plan: ## Preview infrastructure changes
	cd terraform && terraform plan

terraform-apply: ## Create GCS bucket and BigQuery dataset on GCP
	cd terraform && terraform apply

terraform-destroy: ## Tear down all GCP resources
	cd terraform && terraform destroy

# ── Environment ─────────────────────────────────────────────────────

generate-env: ## Generate airflow/.env from Terraform outputs
	cd terraform && bash generate_env.sh

# ── Airflow ─────────────────────────────────────────────────────────

airflow-build: ## Build the custom Airflow Docker image
	cd airflow && docker-compose build

airflow-up: ## Start all Airflow services (detached)
	cd airflow && docker-compose up -d

airflow-down: ## Stop all Airflow services
	cd airflow && docker-compose down

airflow-reset: ## Full reset — stop, remove volumes, rebuild, start
	cd airflow && docker-compose down -v && docker-compose build && docker-compose up -d

airflow-logs: ## Tail scheduler logs
	cd airflow && docker-compose logs -f airflow-scheduler
