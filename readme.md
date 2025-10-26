# Game Growth Analytics

End-to-end data pipeline games analytics for user growth, retention. Working with kaggle dataset L : \n
```
https://www.kaggle.com/datasets/debs2x/gamelytics-mobile-analytics-challenge/data
```

#### Using: 
####   1st : Snowflake, DBT, Airflow and PowerBI
#### Then : 
####   2nd : Terraform, S3, Glue, Redshift, DBT, PowerBI

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


