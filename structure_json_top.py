import json 

with open('JSON/sorted_JSON_headings.json') as f:
    data = json.load(f)


new_dict = {}
count_dict = {}


for key, value in data.items():
    for keys, item in value.items():
        if not item < 10:
            count_dict[keys] = item
    new_dict[key] = count_dict
    count_dict = {}

        

with open("JSON/sorted_JSON_headings_top.json", "w") as json_file:
    json.dump(new_dict, json_file)