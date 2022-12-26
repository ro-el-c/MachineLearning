from dataclasses import replace
import os
import sys
import json
from unittest.mock import sentinel

dir_path = "./201911278_정경은/031.온라인 구어체 말뭉치 데이터/01.데이터/1.Training_220728_add/원천데이터/TS1/유머"

data = []
dataToAppend = ""

lines=0

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(dir_path, file)
        #print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f: # 각 json 파일 open

            json_data = json.load(f)

            for i in range(100): # 5로 수정 - 여러 파일에서 데이터를 가져오기 위하여 제한
                if i >= len(json_data['SJML']['text']):
                    break

                json_text_data = json_data['SJML']['text'][i]['content']
                sentence_list = json.dumps(json_text_data, indent="\t", ensure_ascii=False).split(" . . ")

                sentence_list = sentence_list[len(sentence_list)//3].split(". ")
                sentence_list = sentence_list[len(sentence_list)//2].split(".")
                sentence = sentence_list[len(sentence_list)//3]

                sentence = sentence[1:-1].strip()
                
                if sentence == "" or len(sentence) >= 20:
                    continue

                elif lines%2 == 0:
                    print("lines: {0}, sentence: {1}".format(lines, sentence))

                    tempSentence = ""
                    # TODO: 문장 수정 띄어쓰기에는 <SP>
                    for i in range(len(sentence)):
                        unit = sentence[i]
                        if unit == " ":
                            tempSentence += "<SP> "
                        else:
                            tempSentence += unit + " "
                    
                    
                    dataToAppend = tempSentence.strip()

                    lines+=1

                else:
                    print("lines: {0}, label: {1}".format(lines, sentence))

                    tempSentence = ""
                    # TODO: 문장 수정 띄어쓰기에는 <SP>
                    for i in range(len(sentence)):
                        unit = sentence[i]
                        if unit == " ":
                            tempSentence += "<SP> "
                        else:
                            tempSentence += unit + " "

                    dataToAppend +=  "\t" + tempSentence + "</S>\n"
                    #print(dataToAppend)

                    # 전처리 된 문장 추가
                    data.append(dataToAppend)
                    dataToAppend = ""

                    lines+=1

                if lines >= 20000: # 20000줄 -> 2개씩 (sentence & label) 한 쌍이 되어 총 10000줄의 데이터가 됨
                    break

            if lines >= 20000:
                break

        if lines >= 20000:
            break
    if lines >= 20000:
        break


# 전처리 완료 데이터 Json 파일로 저장
lines=0
train_file = open("./train.txt", "w", encoding='utf-8')
max_length = 0
for temp in data:
    if len(temp) > max_length:
        max_length = len(temp)

    lines += 1
    train_file.write(temp)
train_file.close()

"""
with open("./train.txt", "r") as file:
    data = file.read()
    print(data)
"""

print()
print()
print("lines:", lines)
print("max_length:", max_length)