import json
# リストに格納
gen_dict = {}
for i in range(64):
    if i == 0:
        gen_dict[i] = {}
    else:
        gen_dict[i] = {}

for i in range(64):
    gen_dict[i] = {}
    for j in range(64):
        gen_dict[i][j] = {}
        
#print(gen_dict)

with open('record.json', 'w') as f:
    json.dump(gen_dict, f, indent=4)