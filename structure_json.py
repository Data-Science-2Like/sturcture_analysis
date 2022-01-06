import json 

with open('JSON/section_headings.json') as f:
    data = json.load(f)


new_dict = {}
count_dict = {}


for key, value in data.items():
    for item in value:
        if item not in count_dict:
            count_dict[item] = 1
        else:
            count_dict[item] += 1

    new_dict[key] = count_dict
    count_dict = {}
        

with open("JSON/sorted_JSON_headings.json", "w") as json_file:
    json.dump(new_dict, json_file)