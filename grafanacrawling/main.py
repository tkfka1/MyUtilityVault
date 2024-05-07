import requests
from bs4 import BeautifulSoup

# 웹 페이지 URL
url = ''

# requests를 사용하여 웹 페이지의 내용을 가져옴
response = requests.get(url)
response.raise_for_status()  # 요청에 실패한 경우 예외를 발생시킴

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, 'html.parser')

# 웹 페이지의 제목 태그(<title>) 내용을 추출

data = response.json()

# 데이터 출력
print(data)