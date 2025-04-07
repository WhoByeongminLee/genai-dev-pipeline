# meta/config/settings.py

SOURCE_BUCKET = 'ks2-kai-dev-kabie-s3-agent'
TARGET_BUCKET = 'ks2-kai-dev-kabie-s3-agent'
BASE_PREFIX = 'incpyjbinvt/mrktg'

DATA_ID_RANGE = range(1, 17 + 1)  # 0001 ~ 0017

S3_PATH_RULE = {
    "raw": "{base_prefix}/raw/{data_id}/{year}/{yyyymm}/{yyyymmdd}/",
    "prpr": "{base_prefix}/prpr/{data_id}/{year}/{yyyymm}/{yyyymmdd}/",
    "log": "{base_prefix}/log/{data_id}/{year}/{yyyymm}/{yyyymmdd}/"
}