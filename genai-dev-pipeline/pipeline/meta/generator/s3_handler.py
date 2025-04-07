# meta/generator/s3_handler.py

import boto3
import os
from meta.generator.s3_path_resolver import S3PathResolver

class S3Handler:
    def __init__(self, source_bucket: str, target_bucket: str, base_prefix: str = ""):
        self.s3 = boto3.client('s3')
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket
        self.base_prefix = base_prefix

    def list_source_files(self, data_id: str, target_date: str) -> list:
        prefix = S3PathResolver.resolve("raw", data_id, target_date)
        paginator = self.s3.get_paginator('list_objects_v2')
        result = []
        for page in paginator.paginate(Bucket=self.source_bucket, Prefix=prefix):
            for content in page.get('Contents', []):
                result.append(content['Key'])
        return result

    def copy_file(self, source_key: str, data_id: str, target_date: str, renamed_file: str):
        target_prefix = S3PathResolver.resolve("prpr", data_id, target_date)
        target_key = f"{target_prefix}{renamed_file}"
        copy_source = {'Bucket': self.source_bucket, 'Key': source_key}
        self.s3.copy_object(CopySource=copy_source, Bucket=self.target_bucket, Key=target_key)
        return target_key

    def upload_metadata(self, metadata_content: str, data_id: str, target_date: str, metadata_file: str):
        target_prefix = S3PathResolver.resolve("prpr", data_id, target_date)
        target_key = f"{target_prefix}{metadata_file}"
        self.s3.put_object(Bucket=self.target_bucket, Key=target_key, Body=metadata_content.encode('utf-8'))

    def upload_log(self, log_content: str, data_id: str, target_date: str):
        # log/DT_AIG_0001/2025/202504/20250401/meta_20250401123045.log
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        log_prefix = S3PathResolver.resolve("log", data_id, target_date)
        log_key = f"{log_prefix}meta_{timestamp}.log"
        self.s3.put_object(Bucket=self.target_bucket, Key=log_key, Body=log_content.encode("utf-8"))
        return log_key

    def get_file_size(self, key: str) -> int:
        response = self.s3.head_object(Bucket=self.source_bucket, Key=key)
        return response['ContentLength']