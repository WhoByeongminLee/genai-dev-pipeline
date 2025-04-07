# meta/generator/s3_path_resolver.py

from datetime import datetime
from meta.config.settings import S3_PATH_RULE, BASE_PREFIX

class S3PathResolver:
    @staticmethod
    def resolve(folder_type: str, data_id: str, date_str: str) -> str:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        year = dt.strftime("%Y")
        yyyymm = dt.strftime("%Y%m")
        yyyymmdd = dt.strftime("%Y%m%d")

        rule = S3_PATH_RULE.get(folder_type)
        if not rule:
            raise ValueError(f"Unsupported folder_type: {folder_type}")

        return rule.format(
            base_prefix=BASE_PREFIX,
            data_id=data_id,
            year=year,
            yyyymm=yyyymm,
            yyyymmdd=yyyymmdd
        )