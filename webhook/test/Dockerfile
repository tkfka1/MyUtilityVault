# Dockerfile
FROM public.ecr.aws/lambda/python:3.12

# 현재 디렉토리의 모든 파일을 컨테이너에 복사합니다.
COPY . .

# Lambda 함수 핸들러를 환경 변수로 설정합니다.
ENV HANDLER_FILE=app.lambda_handler

# Lambda 런타임에서 기본적으로 제공하는 명령어로 이미지를 실행합니다.
CMD ["app.lambda_handler"]
