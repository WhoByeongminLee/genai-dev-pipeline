import os
from datetime import datetime

class FileRenamer:
    def __init__(self):
        self.business_code = "KS2"
        self.max_length = 255

    def generate_original_filename(self, original_key: str) -> str:
        """
        원본 S3 Key → 전송용 파일명 생성
        포맷: KS2_파일명_YYYYMMDDHHMMSS.확장자
        255자 초과 시 오른쪽 잘라냄
        """
        base_name = os.path.basename(original_key)
        file_name, ext = os.path.splitext(base_name)
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")

        ext = ext.lstrip('.')
        new_name = f"{self.business_code}_{file_name}_{current_time}.{ext}"

        if len(new_name) > self.max_length:
            excess_length = len(new_name) - self.max_length
            file_name_trimmed = file_name[:-excess_length] if excess_length < len(file_name) else ""
            new_name = f"{self.business_code}_{file_name_trimmed}_{current_time}.{ext}"

        return new_name