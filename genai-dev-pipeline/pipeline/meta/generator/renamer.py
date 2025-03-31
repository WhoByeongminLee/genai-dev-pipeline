# pipeline/meta/generator/renamer.py

import os
from datetime import datetime


class FileRenamer:
    def __init__(self, data_id: str, target_date: str):
        self.data_id = data_id
        self.target_date = target_date
        self.business_code = "KS2"
        self.max_length = 255

    def rename(self, index: int, original_ext: str) -> str:
        index_str = str(index).zfill(4)
        return f"{self.data_id}_{self.target_date}_{index_str}.{original_ext}"

    def generate_original_filename(self, original_key: str) -> str:
        base_name = os.path.basename(original_key)
        file_name, ext = os.path.splitext(base_name)
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")

        new_name = f"{self.business_code}_{file_name}_{current_time}{ext}"

        # 제약사항 처리: 255자 이하로 잘라내기
        if len(new_name) > self.max_length:
            # 확장자는 유지하고, 파일명 오른쪽을 잘라냄
            excess_length = len(new_name) - self.max_length
            file_name_trimmed = (
                file_name[:-excess_length] if excess_length < len(file_name) else ""
            )
            new_name = f"{self.business_code}_{file_name_trimmed}_{current_time}{ext}"

        return new_name
