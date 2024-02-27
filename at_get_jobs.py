import json
import requests
from nltk.translate.bleu_score import sentence_bleu


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
jobs_arr = []
def readJobs(path):
    with open(path,"r", encoding="utf-8") as f:
        jobs = f.read().splitlines()
        for job in jobs:
           data = json.loads(job.replace("\'", "\""))
           jobs_arr.append(data["data"]["jobId"])

translated_strings=[]

def read_jobs():
    for job in jobs_arr:
        url_post =  'http://192.168.2.232:8000/v2/ai/model/job?job_id='+str(job)
        headers = {"Authorization": "Basic YmVuejpCM256QDEyMw=="}
        post_response = requests.get(url_post,headers=headers)
        response_json = post_response.json()
        translated_strings.append(response_json["data"]["output"]["translations"][0]["translatedText"])

def compare():
    with open('mt.txt', 'w', encoding="utf-8") as f:
        for mt, manual in zip(translated_strings, ta01["story"]):
            print("mt",mt)
            print("manual",manual["text"])
            f.write(f"{mt}\n")
            print(sentence_bleu([mt.split()], manual["text"].split()))

readJobs(r"jobs.txt")
read_jobs()
ta01=readMDFile(r"tam\content\01.md")
# print(json.dumps(ta01, indent=2))
compare()

