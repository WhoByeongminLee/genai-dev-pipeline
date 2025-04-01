# pipeline/meta/infra/lambda_trigger.py

import boto3
from datetime import datetime


def lambda_handler(event, context):
    # SageMaker 클라이언트 생성
    sagemaker_client = boto3.client("sagemaker")

    # Job 이름: 실행 시마다 고유하게 생성
    job_name = f"meta-pipeline-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Processing Job 생성
    response = sagemaker_client.create_processing_job(
        ProcessingJobName=job_name,
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.t3.mediulsm",
                "VolumeSizeInGB": 10,
            }
        },
        AppSpecification={
            "ImageUri": "YOUR-SAGEMAKER-IMAGE-URI",
            "ContainerEntrypoint": [
                "python3",
                "/opt/ml/processing/input/run_meta_pipeline.py",
            ],
        },
        RoleArn="YOUR_SAGEMAKER_ROLE_ARN",
        ProcessingInputs=[
            {
                "InputName": "input-1",
                "S3Input": {
                    "S3Uri": "s3://your-bucket/meta-scripts/",
                    "LocalPath": "/opt/ml/processing/input",
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                },
            }
        ],
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "logs",
                    "S3Output": {
                        "S3Uri": "s3://your-bucket/meta-logs/",
                        "LocalPath": "/opt/ml/processing/output",
                        "S3UploadMode": "EndOfJob",
                    },
                }
            ]
        },
    )

    print(f"[INFO] Processing Job Started: {job_name}")
    print(response)