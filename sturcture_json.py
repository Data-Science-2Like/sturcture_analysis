import json 

with open('JSON/section_headings.json') as f:
    data = json.load(f)


new_dict = {}
empty_list = 1
# empty_list = [0,0,0,0,0,0,0,0]

for x in data.values():
    for y in x:
        if y in new_dict:
            new_dict[y] += 1
        if y not in new_dict:
            y = { y : empty_list}
            new_dict.update(y)
        
        

with open("JSON/sorted_JSON_headings.json", "w") as json_file:
    json.dump(new_dict, json_file)