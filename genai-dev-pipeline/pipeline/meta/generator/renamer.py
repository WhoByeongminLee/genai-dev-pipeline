class FileRenamer:
    def __init__(self, data_id: str, target_date: str):
        self.data_id = data_id
        self.target_date = target_date

    def rename(self, index: int, original_ext: str) -> str:
        index_str = str(index).zfill(4)
        return f"{self.data_id}_{self.target_date}_{index_str}.{original_ext}"