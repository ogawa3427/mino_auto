import json

with open('log.json', 'r') as f:
    data = json.load(f)

for i in range(64):
    for j in range(12):
        print(data[str(i)][str(j)])