import images_to_pdf
import send_email_with_attachment
from configparser import ConfigParser
import os

path = "#input/"
output = '#output/output.pdf'

config = ConfigParser()
# config.load('config.ini')

# print(config['Email']['send_from']) # value_1

def find_image_files(directory):
    # 지원하는 이미지 파일 확장자 목록
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_files = []

    # 주어진 디렉토리를 순회하며 파일 검색
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                # 전체 파일 경로를 리스트에 추가
                image_files.append(os.path.join(root, file))

    return image_files

print(find_image_files(path))

# 이미지 파일 목록과 PDF 이름 지정
# image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg']
image_files = find_image_files(path)
output_pdf = output

# 이미지를 PDF로 변환
images_to_pdf.images_to_pdf(image_files, output_pdf)

# # 이메일 설정
# send_from = 'your_email@gmail.com'
# send_to = 'receiver_email@gmail.com'
# subject = 'Here is your PDF'
# body = 'Attached the PDF converted from images.'
# files = [output_pdf]
# server = 'smtp.gmail.com'
# port = 465
# username = 'your_email@gmail.com'
# password = 'your_app_password'  # 구글 애플리케이션 별 비밀번호

# # 이메일 전송
# send_email_with_attachment.send_email_with_attachment(send_from, send_to, subject, body, files, server, port, username, password)