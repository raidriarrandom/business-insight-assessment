import boto3
import time
import pandas as pd

def run_athena_query(query, database="business_assessment_db", region="us-west-1"):
    client = boto3.client("athena", region_name=region)

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database},
        ResultConfiguration={"OutputLocation": "s3://business-insight-assessment-499502048569/athena-query-results/"}
    )
    query_id = response["QueryExecutionId"]

    while True:
        status = client.get_query_execution(QueryExecutionId=query_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)

    if state != "SUCCEEDED":
        raise Exception(f"Athena query failed: {status['QueryExecution']['Status'].get('StateChangeReason')}")

    results = client.get_query_results(QueryExecutionId=query_id)
    columns = [col["Label"] for col in results["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]]
    rows = []
    for row in results["ResultSet"]["Rows"][1:]:
        rows.append([field.get("VarCharValue", None) for field in row["Data"]])

    return pd.DataFrame(rows, columns=columns)


