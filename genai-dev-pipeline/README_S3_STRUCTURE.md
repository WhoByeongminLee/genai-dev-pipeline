
# S3 버킷 구조 안내 (RAG 문서 적재용)

본 S3 버킷은 RAG 서비스 구축을 위한 문서 데이터를 수집, 가공, 메타파일 생성의 전처리 파이프라인을 지원하기 위해 설계되었습니다.

## 버킷명
aig-rag-data-prod

## 폴더 구조
```
s3://aig-rag-data-prod/
├── raw/
│   ├── DT_AIG_0001/
│   │   └── YYYY-MM-DD/
│   │       └── 원본파일.xlsx
│   ├── DT_AIG_0002/
│   └── ...
├── processed/
│   ├── DT_AIG_0001/
│   │   └── YYYY-MM-DD/
│   │       ├── KS2_원본파일_YYYYMMDDHHMMSS.xlsx
│   │       └── KS2_원본파일_YYYYMMDDHHMMSS.xlsx.json
│   ├── DT_AIG_0002/
│   └── ...
└── logs/
    ├── ingestion/
    │   └── YYYY-MM-DD.log
    └── processing/
        └── YYYY-MM-DD.log
```

## 폴더 설명
- **raw/**: 데이터 수집 파이프라인을 통해 수집된 원본 파일을 저장
- **processed/**: 파일명 표준화 및 메타파일 생성 후 저장
- **logs/**: 일배치 작업의 적재 및 처리 로그 파일 저장

## 파일명 규칙
### 원본파일 (raw)
수집된 원본 파일 그대로 저장

### 가공파일 (processed)
```
KS2_{원본파일명}_{YYYYMMDDHHMMSS}.{확장자}
```
예시: `KS2_금지어와 대체어_202412 ver_251203053210.xlsx`

### 메타파일 (processed)
가공파일과 동일한 이름에 `.json` 확장자 추가
예시: `KS2_금지어와 대체어_202412 ver_251203053210.xlsx.json`

### 로그파일
```
ingestion/YYYY-MM-DD.log
processing/YYYY-MM-DD.log
```

## 배치 운영 원칙
- 데이터 적재 및 가공은 **일배치 기준**
- 원본 파일은 **절대 수정 불가**, 가공파일과 메타파일은 processed 경로에 별도 저장
- 장애 발생 시 logs 폴더에서 일자별 로그 확인 가능

## 추가 참고
- DT_AIG_0001 ~ DT_AIG_0016 의 데이터 유형에 따라 파일 확장자와 파일명은 상이할 수 있음
- 모든 파이프라인 작업은 추후 Airflow, AWS Batch 등 외부 스케줄러와 연계 가능하도록 설계됨
