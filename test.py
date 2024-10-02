import json

with open("D:\Study\Flask\Link_Shortner\static\links.json", "r") as f:
    file=json.load(f)

print(file.keys())