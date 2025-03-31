
import boto3
import os

class S3Handler:
    def __init__(self, source_bucket: str, target_bucket: str, base_prefix: str = ""):
        # S3 핸들러 초기화 (버킷, prefix)
        self.s3 = boto3.client('s3')
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket
        self.base_prefix = base_prefix

    def list_source_files(self, data_id: str, target_date: str) -> list:
        # 원본 파일 목록 조회
        prefix = f"{self.base_prefix}/raw/{data_id}/{target_date}/"
        paginator = self.s3.get_paginator('list_objects_v2')
        result = []
        for page in paginator.paginate(Bucket=self.source_bucket, Prefix=prefix):
            for content in page.get('Contents', []):
                result.append(content['Key'])
        return result

    def copy_file(self, source_key: str, data_id: str, target_date: str, renamed_file: str):
        # 원본파일 → processed 경로로 복사
        copy_source = {'Bucket': self.source_bucket, 'Key': source_key}
        target_key = f"{self.base_prefix}/processed/{data_id}/{target_date}/{renamed_file}"
        self.s3.copy_object(CopySource=copy_source, Bucket=self.target_bucket, Key=target_key)
        return target_key

    def upload_metadata(self, metadata_content: str, data_id: str, target_date: str, metadata_file: str):
        # 메타파일 업로드
        target_key = f"{self.base_prefix}/processed/{data_id}/{target_date}/{metadata_file}"
        self.s3.put_object(Bucket=self.target_bucket, Key=target_key, Body=metadata_content.encode('utf-8'))

    def get_file_size(self, key: str) -> int:
        # 원본파일 크기 조회
        response = self.s3.head_object(Bucket=self.source_bucket, Key=key)
        return response['ContentLength']
