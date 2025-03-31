1. CloudWatch Events + Lambda + Notebook 실행

AWS에서는 CloudWatch Events (EventBridge) + Lambda를 통해
Notebook 인스턴스 안의 Python Script를 주기적으로 실행하는 방법을 공식적으로 제공함

CloudWatch Events (매일 3시 트리거)
         ↓
AWS Lambda → SageMaker API 호출 → Jupyter Notebook (.py) 스크립트 실행


1) bash: jupyter nbconvert --to script run_meta_pipeline.ipynb
2) CloudWatch Rule 생성 (3시 트리거) - 스케줄: cron(0 18 * * ? *) (UTC 기준, 한국시간 새벽 3시는 UTC 18시)
3) Lambda Function 생성: 
권한 부여: Lambda에 다음 권한 필요
SageMaker: sagemaker:StartNotebookInstance
SageMaker: sagemaker:CreateProcessingJob
CloudWatch Logs
코드예시:

import boto3
def lambda_handler(event, context):
    client = boto3.client('sagemaker')
    response = client.create_processing_job(
        ProcessingJobName='meta-pipeline-job',
        ProcessingResources={
            'ClusterConfig': {
                'InstanceCount': 1,
                'InstanceType': 'ml.t3.medium',
                'VolumeSizeInGB': 10
            }
        },
        AppSpecification={
            'ImageUri': 'YOUR-SAGEMAKER-IMAGE-URI',
            'ContainerEntrypoint': [
                'python3',
                '/opt/ml/processing/input/run_meta_pipeline.py'
            ]
        },
        RoleArn='YOUR_SAGEMAKER_ROLE_ARN',
        ProcessingInputs=[{
            'InputName': 'input-1',
            'S3Input': {
                'S3Uri': 's3://your-bucket/meta-scripts/',
                'LocalPath': '/opt/ml/processing/input',
                'S3DataType': 'S3Prefix',
                'S3InputMode': 'File'
            }
        }],
        ProcessingOutputConfig={
            'Outputs': []
        }
    )
    print(response)


 (선택) Crontab 대안: SageMaker Studio의 Scheduler 사용
최근에는 SageMaker Studio → Schedule Jobs 기능도 제공되어, SageMaker 자체에서 Python Script Scheduling 가능

가장쉽게:
S3에 .py올리고 Lambda+EventBridge Rule 설정
