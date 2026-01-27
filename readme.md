# Game Growth Analytics

End-to-end data pipeline games analytics for user growth, retention. Working with kaggle dataset L : \n

```
https://www.kaggle.com/datasets/debs2x/gamelytics-mobile-analytics-challenge/data
```

#### Using:

#### 1st : Snowflake -> DBT-> Airflow -> PowerBI

#### 2nd : Terraform -> S3 -> Glue -> Redshift -> DBT -> PowerBI

#### 3nd : Local -> GCS -> BigQuery Raw -> Scheduled Queries -> Curated -> Power BI

#### Install Google Cloud SDK then verify

```bash
gcloud --version
```

#### Create or set project

```bash
gcloud project list
gcloud set $PORJECT_ID

```

#### Enable services

```bash
gcloud services enable \
    storage.googleapis.com \
    bigquery.googleapis.com \
    cloudbuild.googleapis.com \
    iam.googleapis.com
```

#### Export variables

```bash
export PROJECT_ID={your_project_id}
export REGION={your_region}
```

PowerShell

```bash
$PROJECT_ID="your_project_id"
$REGION="your_region"
```

#### Create buckets

```bash
gsutil mb -l $REGION gs://$PROJECT_ID-raw
gsutil mb -l $REGION gs://$PROJECT_ID-processed
gsutil mb -l $REGION gs://$PROJECT_ID-dlq
```

#### Create Dataset and tables

```bash
bq mk --dataset $PROJECT_ID:<dataset>
```

Or create it through the console

#### Create services accounts

With Role : BQ User and Storage Object User

#### Copy data to GCS

```bash
gcloud storage ls
```

```bash
gcloud storage cp <file> gs://<bucket>
```

## Architecture Overview

```
S3 Raw
↓ Glue (Spark)
S3 Curated (Parquet)
↓ COPY
Redshift Serverless (Staging)
↓ dbt
Analytics
↓
Power BI Dashboards
```

#### 1st pipeline with Snowflake, DBT, Airflow :

<img width="1325" height="550" alt="image" src="https://github.com/user-attachments/assets/8197f40d-0477-4af3-b38d-7e058ed4666b" />

## 2nd pipeline with Snowflake, DBT, Airflow :

### Technologies: AWS (S3, Redshift Serverless, IAM), Terraform, dbt Core, Power BI

#### Deploy Infrastructure (Terraform)

```bash
cd aws_infra
terraform init
terraform apply
```

#### Creates:

- VPC
- Redshift Serverless
- IAM role for COPY
- S3 buckets (curated + temp)

#### Load Data into Redshift

Example:

```
COPY staging.registration
FROM 's3://game-growth-curated/reg_data/'
IAM_ROLE '<role-arn>'
FORMAT AS PARQUET;
```

#### Validate:

```
SELECT TOP 10
    *
FROM staging.registration;
```

#### dbt Usage

Install:
`pip install dbt-core dbt-redshift`

#### Run transformations:

```
dbt test --target gg_redshift
dbt run --target gg_redshift
```

#### Generate docs

`dbt docs generate && dbt docs serve`

### PowerBI

<img width="855" height="489" alt="Screenshot 2025-10-19 155905" src="https://github.com/user-attachments/assets/191caeca-d5ac-4122-ac4a-b9ba385ff04e" />
