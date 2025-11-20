import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import (
    PipelineOptions,
    GoogleCloudOptions,
    SetupOptions,
    StandardOptions,
)


def load_sql(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--region', required=True)
    parser.add_argument('--temp_location', required=True)
    parser.add_argument('--sql_path', default='sql_queries/retention_query.sql')
    parser.add_argument('--analytics_dataset', default='analytics')
    parser.add_argument('--table_out', default='retention_results')
    parser.add_argument('--runner', default='DataflowRunner')
    args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    cloud = pipeline_options.view_as(GoogleCloudOptions)
    cloud.project = args.project
    cloud.region = args.region
    cloud.temp_location = args.temp_location

    pipeline_options.view_as(StandardOptions).runner = args.runner
    pipeline_options.view_as(SetupOptions).save_main_session = True

    input_query = load_sql(args.sql_path)

    output_table = f"{args.project}:{args.analytics_dataset}.{args.table_out}"
    output_schema = {
        "fields": [
            {"name": "unique_id",          "type": "INTEGER"},
            {"name": "reg_date",           "type": "DATE"},
            {"name": "auth_date",          "type": "DATE"},
            {"name": "max_retention_date", "type": "INTEGER"},
            {"name": "groups",             "type": "STRING"},
        ]
    }

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "ReadRetentionQuery" >> beam.io.ReadFromBigQuery(
                query=input_query,
                use_standard_sql=True,
            )
            | "WriteRetentionResults" >> beam.io.WriteToBigQuery(
                table=output_table,
                schema=output_schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            )
        )


if __name__ == "__main__":
    run()
