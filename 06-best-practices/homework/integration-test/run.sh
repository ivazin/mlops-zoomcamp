#!/bin/bash

export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

export PIPENV_VERBOSITY=-1

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

export S3_ENDPOINT_URL="http://localhost:4566"
export S3_BACKET="s3://nyc-duration"


# export AWS_ENDPOINT_URL="http://localhost:4566"
# aws s3 ls

aws --endpoint-url=${S3_ENDPOINT_URL} s3 mb ${S3_BACKET}
aws --endpoint-url=${S3_ENDPOINT_URL} s3 ls

cd ../

pipenv run python3 integration_test.py

pipenv run python3 batch.py 2023 01

aws --endpoint-url=${S3_ENDPOINT_URL} s3 rm ${S3_BACKET} --recursive