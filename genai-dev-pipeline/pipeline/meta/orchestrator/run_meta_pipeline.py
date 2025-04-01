import sys
import os
from datetime import datetime, timedelta
import boto3
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from meta_pipeline import MetaPipeline
from config.settings import SOURCE_BUCKET, TARGET_BUCKET, BASE_PREFIX, DATA_ID_RANGE
from generator.s3_handler import S3Handler


def write_log_to_s3(log_content: str, target_date: str):
    # 로그 내용을 S3에 저장
    s3 = boto3.client("s3")
    log_key = f"{BASE_PREFIX}/logs/processing/{target_date}.log"
    s3.put_object(Bucket=TARGET_BUCKET, Key=log_key, Body=log_content.encode("utf-8"))


if __name__ == "__main__":
    start_time = datetime.now()
    target_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    data_ids = [f"DT_AIG_{str(i).zfill(4)}" for i in DATA_ID_RANGE]

    s3_handler = S3Handler(SOURCE_BUCKET, TARGET_BUCKET, BASE_PREFIX)
    logs = []

    processed_count = 0
    skipped_count = 0

    logs.append(f"[START] MetaPipeline Batch - Target Date: {target_date}")
    logs.append(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    for data_id in data_ids:
        source_files = s3_handler.list_source_files(data_id, target_date)
        if not source_files:
            log_msg = f"[SKIP] {data_id} - {target_date} 폴더에 데이터 없음"
            print(log_msg)
            logs.append(log_msg)
            skipped_count += 1
            continue

        log_msg = f"[START] {data_id} - {target_date} 처리 시작"
        print(log_msg)
        logs.append(log_msg)

        try:
            pipeline = MetaPipeline(data_id, target_date)
            pipeline.run()
            log_msg = f"[DONE] {data_id} - 파일 {len(source_files)}건 처리 완료"
            print(log_msg)
            logs.append(log_msg)
            processed_count += 1
        except Exception as e:
            log_msg = f"[ERROR] {data_id} - {str(e)}"
            print(log_msg)
            logs.append(log_msg)

    end_time = datetime.now()
    elapsed = end_time - start_time

    # 요약 로그
    logs.append("\n[SUMMARY]")
    logs.append(f"총 데이터설계번호: {len(data_ids)}")
    logs.append(f"처리 완료: {processed_count}")
    logs.append(f"스킵: {skipped_count}")
    logs.append(f"시작 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logs.append(f"종료 시간: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logs.append(f"전체 소요 시간: {str(elapsed)}")

    # S3에 로그 저장
    full_log = "\n".join(logs)
    write_log_to_s3(full_log, target_date)

    print("[INFO] 배치 작업 완료. 로그 저장 완료.")
