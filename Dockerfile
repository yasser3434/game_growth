FROM apache/airflow:2.9.2-python3.11

USER root

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && apt-get clean

USER airflow

RUN pip install \
    dbt-snowflake