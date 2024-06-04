import csv
import re
from datetime import datetime

x = "sosp"

# Read the text file
with open(f'#input/text/{x}.txt', 'r', encoding='utf-8') as file:
    text_data = file.read()

blocks = text_data.strip().split("고객사명 : ")
li = []

for i in blocks:
    ii = i.strip().split("\n")
    if len(ii[0]) > 5:
        if ii[0][:4] == "Shin":
            dic = {}
            dic["고객사명"] = ii[0]
            if ii[2][:4] == ":총격전":
                dic["상태"] = "알람발생"
            else:
                dic["상태"] = "알람해소"
            dic["계정 ID"] = ii[8]
            dic["서비스명"] = ii[10]
            dic["대상"] = ii[12]
            dic["시각"] = ii[14]
            dic["항목"] = ii[16]
            dic["값"] = ii[18]
            dic["비고"] = ii[19:]
            li.append(dic)

print(li)

# CSV file creation
csv_file = f"#output/text/{x}_data.csv"
csv_columns = ["고객사명", "상태", "계정 ID", "서비스명", "대상", "시각", "항목", "값", "비고"]

try:
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for entry in li:
            writer.writerow(entry)
    print(f"CSV file '{csv_file}' created successfully.")
except IOError:
    print("I/O error occurred while creating the CSV file.")