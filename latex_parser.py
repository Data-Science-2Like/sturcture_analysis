from TexSoup import TexSoup
import logging
import os
import datetime
import re
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/parser_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
# Set up directory for LaTex Input
directory = "Latex2"
texfiles = []
template_list = [
    "Introduction", 
    "Related Work", 
    "Methods", 
    "Models", 
    "Experimental Apparatus", 
    "Results",
    "Discussion",
    "Conclusion"
    ]


logger.info("Append LaTex Files to List")
# Iterate over files in directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Checking if it is a file
    if os.path.isfile(f):
        logger.debug(f)
        texfiles.append(f)

# Load File into Soup
# TODO file input muss robuster werden
logger.info("Load LaTex File into Soup")
# Create Dictionary to store soup objects
soup_dict = {}
# Iterate through all TexFiles and place them in dict
for i,item in enumerate(texfiles):
    try:
        soup = TexSoup(open(item))
        # logger.debug(soup)
        # TODO Use title as variable name?? is this usefull??
        # titel = soup.find('title')
        # key = titel.string
        soup_dict[i] = soup
    except TypeError:
        logger.debug("TypeError:")
        logger.debug(f"Doc #{i}: {item} could not be loaded.")
    except:
        logger.debug(f"Doc #{i}: {item} could not be loaded.")
    
#logger.debug(soup_dict)
logger.info("Soup objects successfully loaded into dicctionary.")
logger.info(f"Dicctionary Size: {len(soup_dict)}")


section_dict = {
    0 : [],
    1 : [],
    2 : [],
    3 : [],
    4 : [],
    5 : [],
    6 : [],
    7 : [],
    8 : [],
    9 : [],
    10 : [],
    11 : [],
    12 : [],
    13 : [],
    14 : [],
    15 : [],
    16 : [],
    17 : [],
    18 : [],
    19 : [],
    20 : []
}

logger.info("Find elements in Tex file")
# Iterate through every soup object and extract Section Headings
for soup in soup_dict.values():
    section_list = list(soup.find_all('section'))
    logger.info(section_list)


    # Iterate through all Section Headings and compare to template list
    for i, x in enumerate(section_list):
        clean_string = re.sub('[^A-Za-z0-9 ]+', '', x.string)
        section_dict[i].append(clean_string)

        #print(set(clean_string).intersection(set(template_list)))
        
        # if clean_string.lower() == template_list[i].lower():
        #     print(True, "|" ,template_list[i], " -:- ", clean_string)
        # else:
        #     print(False, "|" , template_list[i], " -:- ", clean_string)


        # print(f"Section heading: {clean_string}")
        # if clean_string.lower() == "introduction":
        #     print(f"Match found: {clean_string}")
        
        # elif clean_string.lower() == "related work":
        #     print(f"Match found: {clean_string}")
 
        # # Methodology added
        # elif clean_string.lower() == "methods" or clean_string.lower() == "methodology":
        #     print(f"Match found: {clean_string}")
 
        # elif clean_string.lower() == "models":
        #     print(f"Match found: {clean_string}")
 
        # elif clean_string.lower() == "experimental apparatus" or clean_string.lower() == "experiments":
        #     print(f"Match found: {clean_string}")
 
        # elif clean_string.lower() == "results":
        #     print(f"Match found: {clean_string}")
 
        # elif clean_string.lower() == "discussison":
        #     print(f"Match found: {clean_string}")
 
        # elif clean_string.lower() == "conclusion" or clean_string.lower() == "conclusion and future work":
        #     print(f"Match found: {clean_string}")
        
        # # Acknowledgement added
        # elif clean_string.lower() == "acknowledgement":
        #     print(f"Match found: {clean_string}")

        # else:
        #     print(f"No match found: {clean_string}")
        
        # print("\n")

    # print("=====================================================")
    # print(section_dict)


# Write Sections to JSON File
json_data = json.dumps(section_dict, indent = 4)
with open("section_headings.json", "w") as outfile:
    outfile.write(json_data)






# Find Elements in LaTex File --------------------
# Load complete Document into "alls"
# alls = soup.all
# logger.debug(alls)
# for x in range(20):
#     print(alls[x])


# subsection_list = list(soup.find_all('subsection'))
# # logger.debug(subsection_list)
 
# abstract = soup.find('abstract')
# # logger.debug(abstract)

# citations_list = list(soup.find_all('cite'))
# # logger.debug(citations_list)
# # for x in citations_list:
# #     print(x)




