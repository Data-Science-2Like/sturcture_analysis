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
#
# TODO file input muss robuster werden
#
logger.info("Load LaTex File into Soup")
# Create Dictionary to store soup objects
soup_dict = {}

# TODO create dynamically?
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
    20 : [],
    21 : [],
    22 : [],
    23 : [],
    24 : [],
    25 : []  
}

# Iterate through all TexFiles and place them in dict
def parse_for_section_headings():
    for i,item in enumerate(texfiles):
        try:
            #logger.debug(f"Load {item} into soup.")
            soup = TexSoup(open(item))

            section_list = list(soup.find_all('section'))
            #logger.info(section_list)

            # TODO 10 Sections die am öftesten vorkommen
            # TODO Ausgabe anders formatieren
            # Iterate through all Section Headings and compare to template list
            for i, x in enumerate(section_list):
                clean_string = re.sub('[^A-Za-z0-9 ]+', '', x.string)
                section_dict[i].append(clean_string)
                section_dict[i].sort()

        except TypeError:
            logger.debug("TypeError:")
            logger.debug(f"Doc #{i}: {item} could not be loaded.")
        except:
            logger.debug(f"Doc #{i}: {item} could not be loaded.")

def compare_with_template():
    for i,item in enumerate(texfiles):
        try:
            #logger.debug(f"Load {item} into soup.")
            soup = TexSoup(open(item))

            section_list = list(soup.find_all('section'))
            #logger.info(section_list)

            # TODO Ausgabe erweiteren - Reihenfolge ausgeben 
            # TODO Input Template auslagern
            # TODO Statistik über Paper erstellen welche Sections vorkommen

            # Iterate through all Section Headings and compare to template list
            for j, x in enumerate(section_list):
                clean_string = re.sub('[^A-Za-z0-9 ]+', '', x.string)
                
                # if clean_string.lower() == template_list[i].lower():
                #     logger.info(True, "|" ,template_list[i], " -:- ", clean_string)
                # else:
                #     logger.info(False, "|" , template_list[i], " -:- ", clean_string)


                logger.info(f"Document # {i}")
                if clean_string.lower() == "introduction":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
                
                elif clean_string.lower() == "related work":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                # Methodology added
                elif clean_string.lower() == "methods" or clean_string.lower() == "methodology":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                elif clean_string.lower() == "models":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                elif clean_string.lower() == "experimental apparatus" or clean_string.lower() == "experiments":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                elif clean_string.lower() == "results":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                elif clean_string.lower() == "discussison":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
        
                elif clean_string.lower() == "conclusion" or clean_string.lower() == "conclusion and future work":
                    logger.info(f"Match found: {clean_string} at Position: {j}")
                
                # Acknowledgement added
                elif clean_string.lower() == "acknowledgement":
                    logger.info(f"Match found: {clean_string} at Position: {j}")

                else:
                    logger.info(f"No match found: {clean_string}")
            logger.debug("===================================================================")

        except TypeError:
            logger.debug("TypeError:")
            logger.debug(f"Doc #{i}: {item} could not be loaded.")
        except Exception as e:
            logger.debug(f"Doc #{i}: {item} could not be loaded: {e}.")


# #logger.debug(soup_dict)
# logger.info("Soup objects successfully loaded into dicctionary.")
# logger.info(f"Dicctionary Size: {len(soup_dict)}")

# logger.info("Find elements in Tex file")
# # Iterate through every soup object and extract Section Headings
# for soup in soup_dict.values():
#     section_list = list(soup.find_all('section'))
#     logger.info(section_list)


#     # Iterate through all Section Headings and compare to template list
#     for i, x in enumerate(section_list):
#         clean_string = re.sub('[^A-Za-z0-9 ]+', '', x.string)
#         section_dict[i].append(clean_string)

        #print(set(clean_string).intersection(set(template_list)))

    # print("=====================================================")
    # print(section_dict)


########################################
# parse_for_section_headings()

# Write Sections to JSON File
# json_data = json.dumps(section_dict, indent = 4)
# with open("section_headings.json", "w") as outfile:
#     outfile.write(json_data)


compare_with_template()



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




