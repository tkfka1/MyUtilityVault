import yaml
import json
import os

def extract_default_values(data):
    """ CloudFormation YAML의 Parameters 섹션에서 기본값 추출 """
    parameters = data.get('Parameters', {})
    default_values = {}
    for key, value in parameters.items():
        default_values[key] = value.get('Default', '')
    return default_values

def convert_yaml_to_json(yaml_file, output_dir):
    # YAML 파일 열기
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # 기본 파라미터 값 추출
    default_values = extract_default_values(data)

    # Resources 부분 추출
    resources = data.get('Resources', {})

    # 각 리소스에 대해 JSON 파일 생성
    for resource_name, details in resources.items():
        properties = details.get('Properties', {})
        config_rule_name = properties.get('ConfigRuleName', resource_name)

        # 입력 파라미터 처리
        input_parameters = properties.get('InputParameters', {})
        for key, value in list(input_parameters.items()):
            if isinstance(value, dict) and 'Fn::If' in value:
                condition_name = value['Fn::If'][0]
                true_value = value['Fn::If'][1].get('Ref')
                false_value = value['Fn::If'][2].get('Ref', '')

                # 조건에 따라 파라미터 값 설정
                input_parameters[key] = default_values.get(true_value, false_value)

        # JSON 파일로 저장
        json_data = {
            "ConfigRuleName": config_rule_name,
            "Source": properties.get('Source', {}),
            "Scope": properties.get('Scope', {}),
            "InputParameters": input_parameters,
            "MaximumExecutionFrequency": properties.get('MaximumExecutionFrequency', ''),
            "Description": properties.get('Description', '')
        }

        # 빈 값 제거
        json_data = {k: v for k, v in json_data.items() if v}

        # 파일명 정의 및 저장
        json_filename = os.path.join(output_dir, f"{config_rule_name}.json")
        with open(json_filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Saved: {json_filename}")

# 사용 예
convert_yaml_to_json('configEX/Operational-Best-Practices-for-KISMS.yaml', 'output')