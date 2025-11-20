import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, GoogleCloudOptions, StandardOptions

def normalize(row: dict) -> dict:
    user_id = int(row.get('user_id')) if row.get('user_id') else None
    revenue = float(row.get('revenue')) if row.get('revenue') else 0.0
    tg = (row.get('testgroup') or '').strip().lower()
    if tg not in ('a', 'b'):
        tg = 'unknown'
    return {
        'user_id': user_id,
        'revenue': revenue,
        'testgroup': tg
    }

def add_revenue_bucket(row: dict) -> dict:
    """Classify user by revenue"""
    revenue = row['revenue']
    if revenue < 10:
        bucket = 'low'
    elif revenue < 50:
        bucket = 'medium'
    else:
        bucket = 'high'
    row['revenue_bucket'] = bucket
    return row

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--region', required=True)
    parser.add_argument('--temp_location', required=True, help='gs://.../tmp')
    parser.add_argument('--staging_dataset', default='staging')
    parser.add_argument('--analytics_dataset', default='analytics')
    parser.add_argument('--table_in', default='ab')
    parser.add_argument('--table_out', default='ab_results')
    parser.add_argument('--runner', default='DataflowRunner')
    args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = args.project
    google_cloud_options.region = args.region
    google_cloud_options.temp_location = args.temp_location
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).runner = args.runner

    input_query = f"""
      SELECT user_id, revenue, testgroup
      FROM `{args.project}.{args.staging_dataset}.{args.table_in}`
    """

    output_table = f"{args.project}:{args.analytics_dataset}.{args.table_out}"
    output_schema = {
        "fields": [
            {"name": "user_id", "type": "INTEGER"},
            {"name": "revenue", "type": "FLOAT"},
            {"name": "testgroup", "type": "STRING"},
            {"name": "revenue_bucket", "type": "STRING"},
        ]
    }

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "ReadFromBigQuery" >> beam.io.ReadFromBigQuery(query=input_query, use_standard_sql=True)
            | "Normalize" >> beam.Map(normalize)
            | "AddRevenueBucket" >> beam.Map(add_revenue_bucket)
            | "WriteToBigQuery" >> beam.io.WriteToBigQuery(
                table=output_table,
                schema=output_schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
            )
        )

if __name__ == "__main__":
    run()
