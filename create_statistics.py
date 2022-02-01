import csv
import json
import matplotlib.pyplot as plt
import statistics

filename = "CSV/sections_headings.csv"

# Read out csv file
with open(filename, 'r') as csvfile:
        # Creating csv writer object
        csvreader = csv.reader(csvfile)

        section_list = []

        for item in csvreader:
            section_list.append(item)

amount_paper = len(section_list)
position_dict = { 
    "0" : [],    
    "1" : [],
    "2" : [],
    "3" : [],
    "4" : [],
    "5" : [],
    "6" : [],
    "7" : [],
    "8" : [],
    "9" : [],
    "10" : []
    }

num_of_headings = { 
    "0" : 0,    
    "1" : 0,
    "2" : 0,
    "3" : 0,
    "4" : 0,
    "5" : 0,
    "6" : 0,
    "7" : 0,
    "8" : 0,
    "9" : 0,
    "10" : 0,
    "11" : 0,
    "12" : 0,
    "13" : 0,
    "14" : 0,
    "15" : 0,
    "16" : 0,
    "17" : 0,
    "18" : 0,
    "19" : 0,
    "20" : 0,
    "21" : 0,
    "22" : 0,
    "23" : 0,
    "24" : 0,
    "25" : 0,
    "26" : 0
    }


section_heading_mean = 0

for item in section_list:
    section_heading_mean += len(item) - 1

    if len(item) < 27:
        num_of_headings[str(len(item))] += 1

    for i, heading in enumerate(item):
        if len(item) > 11:
            continue
        if not heading in position_dict[str(i)]:
            position_dict[str(i)].append(heading)

section_heading_mean = section_heading_mean / amount_paper



plt.bar(num_of_headings.keys(), num_of_headings.values(), color='g' )
plt.title("Number of Sections in Scientific Papers")
plt.xlabel("Number of Sections")
plt.ylabel("Number of Papers")
plt.figtext(0.5, 1, f"Number of Papers: {amount_paper}", ha="center", va="center", fontsize=10)
plt.figtext(0.5, 0.95, f"Section Headings Mean: {round(section_heading_mean, 3)}", ha="center", va="center", fontsize=10)
plt.savefig('CSV/histogram_count_sections.png')
plt.show()



print("Anzahl Paper :" , amount_paper)
print("Durschnittliche Anzahl Headings :" , section_heading_mean)
print("Anzahl Headings im Paper :" , num_of_headings)

json_data = json.dumps(num_of_headings, indent = 4)
with open("JSON/stat_count_pos_head.json", "w") as outfile:
    outfile.write(json_data)