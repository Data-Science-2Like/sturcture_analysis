from TexSoup import TexSoup
import logging
import os
import datetime
import re
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/data_extraction_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
# Set up directory for LaTex Input
directory = "Latex_small"
texfiles = []


logger.info("Append LaTex Files to List")
# Iterate over files in directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Checking if it is a file
    if os.path.isfile(f):
        logger.debug(f)
        texfiles.append(f)

# Load File into Soup
logger.info("Load LaTex File into Soup")

# Create List with Training Documents
D = []
# Create Rule Set
R = []


def load_items_into_soup():
    for i,item in enumerate(texfiles):
        try:
            logger.debug(f"Load {item} into soup.")
            soup = TexSoup(open(item), tolerance=1)
            D.append(soup)

        except Exception as e:
            logger.debug(f"Doc #{i}: {item} could not be loaded.")
            logger.debug("Error occured: "+ str(e))

def iter_through_doc_set():
    # loop until D is empty
    while(D):
        sections = []
        for item in D:
            section_list = list(item.find_all('section'))
            D.remove(item)
        for item in section_list:
            clean_string = re.sub('[^A-Za-z0-9 ]+', '', item.string)
            clean_string = clean_string.lower()   
            # TODO tokenize, lemmatize strings
            sections.append(clean_string)

        if not R:
            R.append(sections)
        else:
            for lists in R:
                for items in lists:
                    pass






    print(R)


        


# Main function calls ===================================================
load_items_into_soup()
iter_through_doc_set()
