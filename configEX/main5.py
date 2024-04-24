import boto3
import json
import subprocess

def deploy_config_rule_from_s3(bucket, key):
    """S3 버킷에서 JSON 파일을 읽고, 그 내용으로 Config 규칙을 배포합니다."""
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)
    config_rule = json.loads(response['Body'].read().decode('utf-8'))

    # InputParameters를 JSON 문자열로 변환
    if 'InputParameters' in config_rule:
        config_rule['InputParameters'] = json.dumps(config_rule['InputParameters'])

    config_rule_str = json.dumps(config_rule)

    # AWS CLI 명령 구성
    command = [
        'aws', 'configservice', 'put-config-rule',
        '--config-rule', config_rule_str
    ]

    # subprocess를 사용하여 명령 실행
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully deployed {key}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to deploy {key}: {e.stderr}")

def main():
    bucket = "config-bucket-699495637884"
    prefix = "Operational-Best-Practices-for-KISMS/"
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    for page in page_iterator:
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.json'):
                deploy_config_rule_from_s3(bucket, key)

if __name__ == "__main__":
    main()