import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from meta_pipeline import MetaPipeline
from config.settings import SOURCE_BUCKET, TARGET_BUCKET

if __name__ == "__main__":
    data_id = "DT0001"
    target_date = datetime.today().strftime("%Y-%m-%d")

    pipeline = MetaPipeline(data_id, target_date, SOURCE_BUCKET, TARGET_BUCKET)
    pipeline.run()
