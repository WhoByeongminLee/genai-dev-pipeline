import boto3


def lambda_handler(event, context):
    sagemaker_client = boto3.client("sagemaker")

    response = sagemaker_client.create_processing_job(
        ProcessingJobName="meta-pipeline-job",
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.t3.medium",
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
        ProcessingOutputConfig={"Outputs": []},
    )

    print(response)
