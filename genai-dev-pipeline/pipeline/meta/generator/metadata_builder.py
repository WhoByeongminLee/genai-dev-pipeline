import json


class MetadataBuilder:
    def __init__(
        self,
        data_id: str,
        target_date: str,
        source_path: str,
        target_path: str,
        file_size: int,
        orcpy_file_name: str,
        extra_info: dict,
    ):
        # 메타데이터 핵심 정보 세팅
        self.data_id = data_id
        self.target_date = target_date
        self.source_path = source_path
        self.target_path = target_path
        self.file_size = file_size
        self.orcpy_file_name = orcpy_file_name
        self.extra_info = extra_info

    def build(self) -> dict:
        # 메타데이터 dict 생성 (필수 키 값 지정)
        base_meta = {
            "gathr_task_ctnt": self.data_id,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "file_size": self.file_size,
            "orcpy_file_name": self.orcpy_file_name,
            "orcpy_file_tag_ctnt": self.extra_info.get("orcpy_file_tag_ctnt", ""),
            "orcpy_file_fxdfm_name": self.extra_info.get("orcpy_file_fxdfm_name", ""),
            "doc_ptm_dstcd": self.extra_info.get("doc_ptm_dstcd", ""),
            "doc_objctv_dstcd": self.extra_info.get("doc_objctv_dstcd", ""),
        }
        return base_meta

    def to_json(self) -> str:
        # JSON 변환
        return json.dumps(self.build(), ensure_ascii=False, indent=2)


""" 예시
{
  "gathr_task_ctnt": "DT_AIG_0001",
  "source_path": "raw/DT_AIG_0001/2025-03-30/original.xlsx",
  "target_path": "processed/DT_AIG_0001/2025-03-30/KS2_original_20250330121212.xlsx",
  "file_size": 123456,
  "orcpy_file_name": "KS2_original_20250330121212.xlsx",
  "orcpy_file_tag_ctnt": "가이드,매뉴얼,금지어,대체어,준수사항",
  "orcpy_file_fxdfm_name": "언어가이드",
  "doc_ptm_dstcd": "05",
  "doc_objctv_dstcd": "2"
}
"""
