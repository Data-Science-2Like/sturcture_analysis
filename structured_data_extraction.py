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
    logger.debug("Size of Corpus : {}".format(len(D)))
    while(D):
        sections = []
        item = D[0]
        section_list = list(item.find_all('section'))
        D.remove(item)
        for item in section_list:
            clean_string = re.sub('[^A-Za-z0-9 ]+', '', item.string)
            clean_string = clean_string.lower()   
            # TODO tokenize, lemmatize strings
            sections.append(clean_string)
        logger.debug("New Sections: {}".format(sections))
        append = False
        
        if not R:
            R.append(sections)
            logger.debug("(1st) New Rule added: {}".format(sections))
        else:
            # R = [[r1],[r2], ...]
            for lists in R:
                intersect = set(lists).intersection(set(sections))
                print(intersect)
                if 
                
                # # r1 = [I, R, M, E]
                # for items in lists:
                #     # l1 = [I, D, M, E]
                #     for items2 in sections:
                        # if items == items2:
                        #     print("Same : ", items)
                        #     logger.debug("Same section heading: "+ items)
                        #     break
                        # else:
                        #     logger.debug("Append = True")
                        #     append = True
                    
            if append == True:
                R.append(sections)
                logger.debug("New Rule added: {}".format(sections))
                append = False
            else:
                logger.debug("No New Rule added.")






    logger.debug("Size of Rule Set : {}".format(len(R)))
    logger.debug("Complete Rule Set: {}".format(R))


        


# Main function calls ===================================================
load_items_into_soup()
iter_through_doc_set()
