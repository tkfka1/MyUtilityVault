import json
import logging
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Slack Webhook URL과 Slack 채널을 환경 변수에서 가져옵니다.
SLACK_HOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
TEAMS_HOOK_URL = os.environ['TEAMS_HOOK_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + json.dumps(event))
    
    # EventBridge 이벤트에서 세부 정보를 추출합니다.
    detail = event.get('detail', {})
    
    instance_id = detail.get('instance-id', 'Unknown Instance')
    state = detail.get('state', 'Unknown State')

    # Slack로 보낼 메시지 형식을 지정합니다.
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': f"EC2 Instance {instance_id} is now {state}"
    }
    
    # Teams로 보낼 메시지 형식을 지정합니다.
    teams_message = {
        'text': f"EC2 Instance {instance_id} is now {state}"
    }

    # Slack에 메시지를 전송합니다.
    req = Request(SLACK_HOOK_URL, json.dumps(slack_message).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
        
    # Teams에 메시지를 전송합니다.
    req = Request(TEAMS_HOOK_URL, json.dumps(teams_message).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to Microsoft Teams")
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
