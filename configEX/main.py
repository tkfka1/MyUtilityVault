import yaml
import json
import os

def save_rule_as_json(rule_name, rule_properties):
    """JSON 파일로 규칙 저장"""
    filename = f"{rule_name}.json"
    with open(filename, 'w') as f:
        json.dump(rule_properties, f, indent=4)
    print(f"Saved {filename}")

def main():
    # YAML 파일 경로
    yaml_file = 'configEX/Operational-Best-Practices-for-KISMS.yaml'

    # YAML 파일을 열고 내용을 로드
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    # 'Resources' 섹션에서 각 규칙을 반복 처리
    for rule_name, rule_content in data['Resources'].items():
        # 'Properties' 항목을 찾아 JSON으로 저장
        if 'Properties' in rule_content:
            save_rule_as_json(rule_name, rule_content['Properties'])

if __name__ == "__main__":
    main()
