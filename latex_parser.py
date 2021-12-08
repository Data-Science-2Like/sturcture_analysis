from TexSoup import TexSoup
import logging
import os
import datetime
import re

# Set up logging
logging.basicConfig(level=logging.INFO, filename="parser_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
# Set up directory for LaTex Input
directory = "Tex Files"
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
for i,item in enumerate(texfiles):
    soup = TexSoup(open(item))
    logger.debug(soup)
    # TODO Use title as variable name?? is this usefull??
    # titel = soup.find('title')
    # key = titel.string
    soup_dict[i] = soup
logger.debug(soup_dict)
logger.info("Soup objects successfully loaded into dicctionary.")
logger.info(f"Dicctionary Size: {len(soup_dict)}")



logger.info("Find elements in Tex file")
for soup in soup_dict.values():
    section_list = list(soup.find_all('section'))
    logger.info(section_list)
    for i, x in enumerate(section_list):
        clean_string = re.sub('[^A-Za-z0-9 ]+', '', x.string)
        if clean_string == template_list[i]:
            print(True)
        else:
            print(False)




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




