

import boto3
import os

class S3Handler:
    def __init__(self, source_bucket: str, target_bucket: str):
        self.s3 = boto3.client('s3')
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket

    def list_source_files(self, prefix: str) -> list:
        paginator = self.s3.get_paginator('list_objects_v2')
        result = []
        for page in paginator.paginate(Bucket=self.source_bucket, Prefix=prefix):
            for content in page.get('Contents', []):
                result.append(content['Key'])
        return result

    def copy_file(self, source_key: str, target_key: str):
        copy_source = {'Bucket': self.source_bucket, 'Key': source_key}
        self.s3.copy_object(CopySource=copy_source, Bucket=self.target_bucket, Key=target_key)

    def upload_metadata(self, metadata_content: str, target_key: str):
        self.s3.put_object(Bucket=self.target_bucket, Key=target_key, Body=metadata_content.encode('utf-8'))

    def get_file_size(self, key: str) -> int:
        response = self.s3.head_object(Bucket=self.source_bucket, Key=key)
        return response['ContentLength']