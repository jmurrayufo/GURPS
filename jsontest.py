import json

with open('data/farmerTemplate.json','rb') as f:
    data=json.load(f)

skills = data["Skills"]
attributes = data["Attributes"]

for i in skills:
    print i
    print skills[i]["weight"]

for i in attributes:
    print i,":",attributes[i]["weight"]