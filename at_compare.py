import json
import requests
from datasets import load_metric

# from nltk.translate.bleu_score import sentence_bleu

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
def read_job_ids(path):
    with open(path,"r", encoding="utf-8") as f:
        jobs = f.read().splitlines()
        for job in jobs:
           data = json.loads(job.replace("\'", "\""))
           jobs_arr.append(data["data"]["jobId"])

translated_strings=[]

def read_job_texts():
    for job in jobs_arr:
        url_post =  'http://192.168.2.232:8000/v2/ai/model/job?job_id='+str(job)
        headers = {"Authorization": "Basic YmVuejpCM256QDEyMw=="}
        post_response = requests.get(url_post,headers=headers)
        response_json = post_response.json()
        translated_strings.append(response_json["data"]["output"]["translations"][0]["translatedText"])

def compare():
    i=1
    # bleu = BLEU(tokenize="none", lowercase=False, smooth="floor")  # Set options according to your needs
    sacrebleu = load_metric("sacrebleu")
    manual_lines=[]
    for item in ta01["story"]:
        lines = item["text"].split("।")
        for line in lines:
            line = line.strip()
            if(line !="" and line!="”" and line !='"'):
                manual_lines.append(line)
    with open('hin_comparison.txt', 'w', encoding="utf-8") as f:
        for mt, manual in zip(translated_strings, manual_lines):
            print(i)
            print("mt",mt)
            print("manual",manual)
            f.write(f"{str(i)}\n")
            f.write(f"Machine Translated:{mt}\n")
            f.write(f"Manual:{manual}\n")
            score = sacrebleu.compute(predictions=[manual],references= [[mt]])
            # score = bleu.compute(
            #     predictions=manual["text"],
            #     references=[mt],
            #     weights=(0, 0, 0.25,0.75),
            # )
            # score = sentence_bleu([mt], manual["text"],weights=(0, 0, 0.25,0.75))
            f.write(f"Score:{str(score)}\n\n")
            print(score)
            i=i+1

read_job_ids(r"jobs_hindi_nllb-600M.txt")
read_job_texts()
ta01=readMDFile(r"hin\content\01.md")
# print(json.dumps(ta01, indent=2))
compare()

