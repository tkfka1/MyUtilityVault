# 파일 열기
with open('text.txt', 'r', encoding='utf-8') as file:
    # 파일 내용 읽기
    content = file.read()

# 공백(스페이스)을 탭으로 변경
content = content.replace('\t', '|')

# 결과를 새 파일에 저장
with open('text.txt', 'w', encoding='utf-8') as file:
    file.write(content)