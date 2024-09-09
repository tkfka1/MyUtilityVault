import json
import logging
import os
import urllib.request
import datetime
from account_dict import account_dict

# Asia/Seoul로 timezone 설정
TZ = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')

# INFO레벨 이상의 로그 메시지만 출력 (INFO, WARNING, ERROR, CRITICAL)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 이벤트 메시지 출력 
def send_message(message, hook_url):
    data = json.dumps(message).encode('utf-8')
    req = urllib.request.Request(hook_url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        print(response_body.decode('utf-8'), response.status)

def get_account_name(account_id):
    return account_dict.get(account_id, "계정정보없음")

def lambda_handler(event, context):
    # 로깅
    logger.info("Event        : " + str(event))
    
    # 기본 정보 추출
    aws_account = event['account']
    account_name = get_account_name(aws_account)
    aws_region = event['region']
    event_time = now
    source = event.get('source', 'Unknown')

    # 이벤트 타입에 따라 다른 처리
    if source == "aws.ec2":
        # EC2 인스턴스 상태 변경
        changed_resource = "EC2"
        instance_id = event['detail']['instance-id']
        state = event['detail']['state']
        ct_url = f"https://{aws_region}.console.aws.amazon.com/ec2/v2/home?region={aws_region}#Instances:instanceId={instance_id}"
        
        # Slack 메시지 전송
        slack_message = {
            "channel": SLACK_CHANNEL,
            "text": f"{changed_resource} 인스턴스 상태 변경이 감지되었습니다.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":bulb:*{changed_resource} 인스턴스 상태 변경이 감지되었습니다.*"
                    }
                },
                {"type": "divider"},
            ],
            "attachments": [{
                "fallback": "Fallback 입니다.",
                "color": "#eb4034" if state in ["terminated", "stopped", "shutting-down"] else "#0c3f7d",
                "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": '*Account*' +'\n' + account_name + " (" + aws_account + ") " + '\n' + aws_region
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Instance ID*' +'\n' + instance_id
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*State*' +'\n' + state
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Time (Asia/Seoul)*' + '\n' + event_time
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "상세 내용 확인  :waving_white_flag:"
                            },
                            "style": "primary",
                            "url": ct_url
                        }
                    ]
                },
                {
                "type": "divider"
                }
                ]
            }]
        }
        send_message(slack_message, SLACK_HOOK_URL)

    elif source == "aws.rds":
        # RDS 이벤트
        changed_resource = "RDS"
        event_id = event['detail']['EventID']
        rds_id = event['detail']['SourceIdentifier']
        event_name = event['detail']['Message']
        ct_url = f"https://{aws_region}.console.aws.amazon.com/rds/home?region={aws_region}#database:id={rds_id}"
        
        slack_message = {
            "channel": SLACK_CHANNEL,
            "text": f"{changed_resource} 변경 사항이 감지되었습니다.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":bulb:*{changed_resource} 변경 사항이 감지되었습니다.*"
                    }
                },
                {"type": "divider"},
            ],
            "attachments": [{
                "fallback": "Fallback 입니다.",
                "color": "#0c3f7d",
                "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": '*Account*' +'\n' + account_name + " (" + aws_account + ") " + '\n' + aws_region
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*RDS Instance ID*' +'\n' + rds_id
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Name*' +'\n' + event_name
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Time (Asia/Seoul)*' + '\n' + event_time
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "상세 내용 확인  :waving_white_flag:"
                            },
                            "style": "primary",
                            "url": ct_url
                        }
                    ]
                },
                {
                "type": "divider"
                }
                ]
            }]
        }
        send_message(slack_message, SLACK_HOOK_URL)

    elif source == "aws.iam":
        # IAM 이벤트
        changed_resource = "IAM"
        event_name = event['detail']['eventName']
        iam_name = event['detail']['requestParameters']['userName']
        ct_url = f"https://{aws_region}.console.aws.amazon.com/iam/home?region={aws_region}#/users/{iam_name}"
        
        slack_message = {
            "channel": SLACK_CHANNEL,
            "text": f"{changed_resource} 변경 사항이 감지되었습니다.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":bulb:*{changed_resource} 변경 사항이 감지되었습니다.*"
                    }
                },
                {"type": "divider"},
            ],
            "attachments": [{
                "fallback": "Fallback 입니다.",
                "color": "#0c3f7d",
                "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": '*Account*' +'\n' + account_name + " (" + aws_account + ") " + '\n' + aws_region
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*IAM User*' +'\n' + iam_name
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Name*' +'\n' + event_name
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Time (Asia/Seoul)*' + '\n' + event_time
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "상세 내용 확인  :waving_white_flag:"
                            },
                            "style": "primary",
                            "url": ct_url
                        }
                    ]
                },
                {
                "type": "divider"
                }
                ]
            }]
        }
        send_message(slack_message, SLACK_HOOK_URL)

    elif source == "aws.security-group":
        # Security Group 이벤트
        if 'ipPermissions' in event['detail']['requestParameters']:
            aws_sg_number = len(event['detail']['requestParameters']['ipPermissions']['items'])
        else:
            aws_sg_number = 1
        
        for i in range(aws_sg_number):
            changed_resource = "Security Group"
            event_name = event['detail']['eventName']
            event_request_parameters = event['detail'].get('requestParameters', {})
            
            aws_sg = event_request_parameters.get('ipPermissions', {}).get('items', [{}])[i]
            aws_sg_depth = aws_sg.get('ipRanges', {}).get('items', [{}])[0]
            aws_sg_id = event['detail']['requestParameters'].get('groupId', "None")
            aws_sg_protocol = aws_sg.get('ipProtocol', 'None')
            aws_sg_fromport = aws_sg.get('fromPort', '0')
            aws_sg_toport = aws_sg.get('toPort', '0')
            aws_sg_ipv4 = aws_sg_depth.get('cidrIp', 'None')
            aws_sg_description = aws_sg_depth.get('description', 'None')

            ct_url = f"https://{aws_region}.console.aws.amazon.com/ec2/v2/home?region={aws_region}#SecurityGroups:groupId={aws_sg_id}"
            
            slack_message = {
                "channel": SLACK_CHANNEL,
                "text": f"{changed_resource} 변경 사항이 감지되었습니다.",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":bulb:*{changed_resource} 변경 사항이 감지되었습니다.*"
                        }
                    },
                    {"type": "divider"},
                ],
                "attachments": [{
                    "fallback": "Fallback 입니다.",
                    "color": "#0c3f7d",
                    "blocks": [
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": '*Account*' +'\n' + account_name + " (" + aws_account + ") " + '\n' + aws_region
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Security Group ID*' +'\n' + aws_sg_id
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Protocol*' +'\n' + aws_sg_protocol
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Port Range*' +'\n' + f"{aws_sg_fromport}-{aws_sg_toport}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*IP Range*' +'\n' + aws_sg_ipv4
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Description*' +'\n' + aws_sg_description
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Event Name*' +'\n' + event_name
                            },
                            {
                                "type": "mrkdwn",
                                "text": '*Event Time (Asia/Seoul)*' + '\n' + event_time
                            }
                        ]
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "상세 내용 확인  :waving_white_flag:"
                                },
                                "style": "primary",
                                "url": ct_url
                            }
                        ]
                    },
                    {
                    "type": "divider"
                    }
                    ]
                }]
            }
            send_message(slack_message, SLACK_HOOK_URL)

    elif source == "aws.signin":
        # AWS Console Login 이벤트
        changed_resource = "AWS 콘솔 로그인"
        user_name = event['detail']['userIdentity']['arn']
        source_ip = event['detail']['sourceIPAddress']
        event_name = event['detail']['eventName']
        login_success = event['detail']['responseElements']['ConsoleLogin']
        login_mfa = event['detail']['additionalEventData']['MFAUsed']
        
        slack_message = {
            "channel": SLACK_CHANNEL,
            "text": f"{changed_resource} 이벤트가 감지되었습니다.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":bulb:*{changed_resource} 이벤트가 감지되었습니다.*"
                    }
                },
                {"type": "divider"},
            ],
            "attachments": [{
                "fallback": "Fallback 입니다.",
                "color": "#0c3f7d",
                "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": '*Account*' +'\n' + account_name + " (" + aws_account + ") " + '\n' + aws_region
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*User Name*' +'\n' + user_name
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Source IP*' +'\n' + source_ip
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Name*' +'\n' + event_name
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Login Success*' +'\n' + login_success
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*MFA Used*' +'\n' + login_mfa
                        },
                        {
                            "type": "mrkdwn",
                            "text": '*Event Time (Asia/Seoul)*' + '\n' + event_time
                        }
                    ]
                },
                {
                    "type": "divider"
                }
                ]
            }]
        }
        send_message(slack_message, SLACK_HOOK_URL)

    else:
        logger.warning("Unhandled event source: " + source)

# 환경변수 설정
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_HOOK_URL = os.getenv('SLACK_HOOK_URL')
