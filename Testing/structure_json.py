import json 
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


with open('JSON/section_headings_main.json') as f:
    data = json.load(f)


new_dict = {}
count_dict = {}


for key, value in data.items():
    for item in value:
        # String completly lowercase
        item = item.lower()    

        # Stemming the Sections to reduce redudancy
        words = nltk.word_tokenize(item)
        stem_sentence = []
        for x in words:
            stem_sentence.append(wordnet_lemmatizer.lemmatize(x))
            stem_sentence.append(" ")
        item = "".join(stem_sentence)

        # Add items to Dict
        if item not in count_dict:
            count_dict[item] = 1
        else:
            count_dict[item] += 1

    new_dict[key] = count_dict
    count_dict = {}
        

with open("JSON/sorted_headings_v2_lemmatizer.json", "w") as json_file:
    json.dump(new_dict, json_file)