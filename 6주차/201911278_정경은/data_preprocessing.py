from dataclasses import replace
import os
import sys
import json
from unittest.mock import sentinel

# 산업, 연예, 경제, 정치, 여행레저, 사회일반, 취미, 건강, 사건사고, 스포츠

dir_list = ['산업', '연예', '경제', '정치', '여행레저', '사회일반', '취미', '건강', '사건사고', '스포츠']
dir_path = "./201911278_정경은/030.웹데이터 기반 한국어 말뭉치 데이터/01.데이터/1.Training/원천데이터/TS1/"

data = []

for catalog in dir_list:
    lines=0
    # data[catalog] = [] # 각 주제별 전처리 과정을 거친 후 저장 될 데이터를 담은 리스트 -> Json 형태로 저장
    for (root, directories, files) in os.walk(dir_path+catalog):
        for file in files:
            file_path = os.path.join(dir_path+catalog, file)
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as f: # 각 json 파일 open

                json_data = json.load(f)
                #print(json.dumps(json_data, indent="\t", ensure_ascii=False))
                    
                for i in range(5): # 5로 수정 - 여러 파일에서 데이터를 가져오기 위하여 제한
                    if i >= len(json_data['SJML']['text']):
                        break

                    json_text_data = json_data['SJML']['text'][i]['content']
                    sentence_list = json.dumps(json_text_data, indent="\t", ensure_ascii=False).split(" . . ")
                    
                    sentence_list = sentence_list[len(sentence_list)//3].split(". ")
                    sentence_list = sentence_list[len(sentence_list)//2].split(".")
                    sentence = sentence_list[len(sentence_list)//3]

                    sentence = sentence.strip(" ") + "."
                    if sentence == "" or len(sentence) < 20:
                        continue
                    else:
                        #print(sentence)
                        tempData = {}
                        tempData['sentence'] = sentence.replace(" ", "").replace("", " ").strip(" ")

                        # 라벨링
                        for i, document in enumerate(sentence):
                            labeling_sentence = []
                            for word in sentence.split(" "):
                                tempWord = ""
                                for i in range(len(word)):
                                    if i == 0:
                                        tempWord += "B "
                                    else:
                                        tempWord += "I "
                                labeling_sentence.append(tempWord)
                            
                        tempData['label'] =  ''.join(labeling_sentence).strip(" ")
                        #print(tempData)

                        # 전처리 된 데이터를 추가
                        data.append(tempData)
                                        
                        lines+=1
                    
                    if lines >= 1000:
                        break

                if lines >= 1000:
                    break

            if lines >= 1000: # 1000으로 수정하기
                break
        if lines >= 1000: # 1000으로 수정하기
            break

# 전처리 완료 데이터 Json 파일로 저장
file_path = "./data_preprocessing.json"
with open(file_path, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii = False)


# spacing_data.txt 로 저장
spacing_data_file = open("./spacing_data.txt", "w", encoding='utf-8')

with open(file_path, 'r', encoding='utf-8') as f: # 처리된 데이터가 저장된 json 파일 open
    json_data = json.load(f)
    #data = json.dumps(json_data, indent="\t", ensure_ascii=False)

    for temp in json_data:
        print(temp)
        spacing_data_file.write(temp['sentence'] + "\t " + temp['label'] + "\n")
        print()
        print()
    
    print(len(json_data))

spacing_data_file.close()

"""with open("./spacing_data.txt", "r") as file:
    data = file.read()
    print(data)"""