# Step 1: Python 이미지 사용
FROM python:3.9-slim

# Step 2: 작업 디렉토리 설정
WORKDIR /app

# Step 3: 필요 패키지 설치
# 일반적으로 AWS Lambda에서 사용할 라이브러리를 requirements.txt로 관리합니다.
# 하지만 여기서는 필요 라이브러리가 기본적으로 포함되어 있기 때문에 생략합니다.

# Step 4: 파이썬 코드 복사
COPY . .

# Step 5: 환경 변수를 설정합니다 (Optional, 실제 환경에서는 CI/CD에서 설정 가능)
# ENV SLACK_WEBHOOK_URL=<your_slack_webhook_url>
# ENV SLACK_CHANNEL=<your_slack_channel>
# ENV TEAMS_HOOK_URL=<your_teams_hook_url>

# Step 6: Lambda 핸들러를 지정 (만약 Lambda에서 사용한다면, 하지만 Docker에서는 직접 실행할 수 있습니다.)
CMD ["python", "lambda_funtion.py"]
