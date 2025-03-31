import json


class MetadataBuilder:
    def __init__(
        self,
        data_id: str,
        target_date: str,
        source_path: str,
        target_path: str,
        file_size: int,
    ):
        self.data_id = data_id
        self.target_date = target_date
        self.source_path = source_path
        self.target_path = target_path
        self.file_size = file_size

    def build(self) -> dict:
        return {
            "data_id": self.data_id,
            "target_date": self.target_date,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "file_size": self.file_size,
        }

    def to_json(self) -> str:
        return json.dumps(self.build(), ensure_ascii=False, indent=2)
