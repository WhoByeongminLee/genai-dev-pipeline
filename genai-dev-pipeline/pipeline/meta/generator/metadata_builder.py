import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from generator.renamer import FileRenamer
from generator.metadata_builder import MetadataBuilder
from generator.s3_handler import S3Handler


class MetaPipeline:
    def __init__(
        self, data_id: str, target_date: str, source_bucket: str, target_bucket: str
    ):
        self.data_id = data_id
        self.target_date = target_date
        self.s3_handler = S3Handler(source_bucket, target_bucket)
        self.renamer = FileRenamer(data_id, target_date)

    def run(self):
        prefix = f"data/{self.data_id}/{self.target_date}/"
        source_files = self.s3_handler.list_source_files(prefix)

        for index, source_key in enumerate(source_files, start=1):
            original_ext = source_key.split(".")[-1]
            renamed_file = self.renamer.rename(index, original_ext)

            target_file_key = (
                f"transmit/{self.data_id}/{self.target_date}/{renamed_file}"
            )
            self.s3_handler.copy_file(source_key, target_file_key)

            file_size = self.s3_handler.get_file_size(source_key)
            metadata = MetadataBuilder(
                data_id=self.data_id,
                target_date=self.target_date,
                source_path=source_key,
                target_path=target_file_key,
                file_size=file_size,
            )
            metadata_key = target_file_key.replace(f".{original_ext}", ".json")
            self.s3_handler.upload_metadata(metadata.to_json(), metadata_key)

            print(f"Processed: {source_key} -> {target_file_key} + metadata")
