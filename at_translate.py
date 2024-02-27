import json
import requests

def readMDFile(path):
    with open(path,"r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    story = { "header":"", "footer":"","story":[]}
    s=[]
    url = ""
    for line in lines:
        if line.startswith("#"):
            story["header"]= line
        elif line.startswith("_"):
            story["footer"]= line
        elif line.strip() != "":
            if line.startswith("![OBS Image]"):
                url = line
            else:
                obj = {"url": url, "text":line}
                s.append(obj)
    story["story"]=s
    return story

jobs = []

def translate(obs):
    story = obs["story"]
    for item in story:
        print(item["text"])
        new_data = [item["text"]]
        url_post =  'http://192.168.2.232:8000/v2/ai/model/text/translate?model_name=nllb-600M&source_language=eng_Latn&target_language=tam_Taml'
        headers = {"Authorization": "Basic YmVuejpCM256QDEyMw=="}

        post_response = requests.post(url_post, json=new_data,headers=headers)

        response_json = post_response.json()
        print(response_json)
        jobs.append(response_json)
    with open('jobs.txt', 'w') as f:
        for job in jobs:
            f.write(f"{job}\n")
# read the file
en01=readMDFile(r"eng\content\01.md")
# translate the individual strings
translate(en01)
# ta01=readMDFile(r"tam\content\01.md")
# print(json.dumps(ta01, indent=2))
# get strings for jobs

