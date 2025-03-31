# pipeline/meta/orchestrator/meta_pipeline.py

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from generator.renamer import FileRenamer
from generator.metadata_builder import MetadataBuilder
from generator.s3_handler import S3Handler
from config.settings import SOURCE_BUCKET, TARGET_BUCKET, BASE_PREFIX
from config.data_catalog import DATA_CATALOG

class MetaPipeline:
    def __init__(self, data_id: str, target_date: str):
        # 파이프라인 초기화
        self.data_id = data_id
        self.target_date = target_date
        self.s3_handler = S3Handler(SOURCE_BUCKET, TARGET_BUCKET, BASE_PREFIX)
        self.renamer = FileRenamer()
        self.catalog_info = DATA_CATALOG.get(data_id, {})  # 해당 데이터ID의 메타정보 가져오기

    def run(self):
        # 메타파이프라인 실행
        source_files = self.s3_handler.list_source_files(self.data_id, self.target_date)

        for source_key in source_files:
            # 전송용 파일명 생성
            renamed_file = self.renamer.generate_original_filename(source_key)

            # 원본파일 → processed 복사
            target_key = self.s3_handler.copy_file(
                source_key, self.data_id, self.target_date, renamed_file
            )

            # 파일 크기 확인
            file_size = self.s3_handler.get_file_size(source_key)

            # 메타데이터 생성
            metadata = MetadataBuilder(
                data_id=self.data_id,
                target_date=self.target_date,
                source_path=source_key,
                target_path=target_key,
                file_size=file_size,
                orcpy_file_name=renamed_file,
                extra_info=self.catalog_info
            )
            metadata_key = renamed_file.replace(f".{renamed_file.split('.')[-1]}", ".json")
            self.s3_handler.upload_metadata(metadata.to_json(), self.data_id, self.target_date, metadata_key)

            print(f"[INFO] Processed: {source_key} → {target_key} + {metadata_key}")