terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ============== BigQuery datasets
resource "google_bigquery_dataset" "staging" {
  dataset_id  = "staging"
  location    = var.location
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id  = "analytics"
  location    = var.location
}

# ============== Buckets 
resource "google_storage_bucket" "dataflow_temp" {
  name                        = "${var.project_id}-dataflow-tmp"
  location                    = var.location
  uniform_bucket_level_access = true
  force_destroy               = true
  lifecycle {
    prevent_destroy = false
  }
}

# ============== Service account to run Dataflow jobs
resource "google_service_account" "dataflow_sa" {
  account_id   = "dataflow-sa"
  display_name = "Dataflow SA"
}

# ============== IAM for Dataflow SA
resource "google_project_iam_member" "df_worker" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

resource "google_project_iam_member" "df_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

resource "google_project_iam_member" "bq_user" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

resource "google_project_iam_member" "bq_jobuser" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}

resource "google_project_iam_member" "storage_objadmin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.dataflow_sa.email}"
}
