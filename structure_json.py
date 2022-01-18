import json 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

 #creating an instance of the class
ps = PorterStemmer()

with open('JSON/section_headings_main.json') as f:
    data = json.load(f)


new_dict = {}
count_dict = {}


for key, value in data.items():
    for item in value:
        item = item.lower()    
        item = ps.stem(item)
        if item not in count_dict:
            count_dict[item] = 1
        else:
            count_dict[item] += 1

    new_dict[key] = count_dict
    count_dict = {}
        

with open("JSON/sorted_headings_v2_stemming.json", "w") as json_file:
    json.dump(new_dict, json_file)