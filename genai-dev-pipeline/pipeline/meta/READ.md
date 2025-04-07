# README.md

# AIG RAG 메타데이터 파이프라인

## 개요
이 프로젝트는 AIG 데이터 수집용 S3 원본 파일을 처리하여
전송 파일과 메타데이터 JSON 파일을 자동으로 생성 및 저장하는 파이프라인입니다.

## 주요 기능
- S3 원본 파일 이름 → 전송 규칙 파일명으로 변경 및 복사
- 메타데이터 파일 자동 생성
- 날짜별, 데이터설계번호별 일괄 처리 가능
- 처리 로그 자동 생성 및 S3에 업로드

## S3 경로 구조
S3 경로는 다음과 같은 Rule 기반으로 동적으로 생성됩니다.

```
/{base_prefix}/raw/{data_id}/{year}/{yyyymm}/{yyyymmdd}/
/{base_prefix}/prpr/{data_id}/{year}/{yyyymm}/{yyyymmdd}/
/{base_prefix}/log/{data_id}/{year}/{yyyymm}/{yyyymmdd}/
```

경로 변경 시 `config/settings.py` 내 `S3_PATH_RULE` 값만 수정하면 전체 파이프라인에 자동 반영됩니다.

## 실행 방법

1. 하루치 전체 일괄 처리 (배치)
```bash
python meta/orchestrator/run_meta_pipeline.py
```

2. SageMaker Lambda 트리거도 지원 (`infra/lambda_trigger.py` 참고)

## 주요 폴더 구조
```
meta/
├── config/         # 설정 파일
├── generator/      # S3 핸들러, 경로 Resolver, 파일명 Generator 등
├── orchestrator/   # 파이프라인 실행
└── infra/          # Lambda Trigger (옵션)
```