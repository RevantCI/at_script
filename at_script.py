import json
def readMDFile(path):
    with open(path) as f:
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
    print(json.dumps(story, indent=2))

readMDFile('eng/content/01.md')