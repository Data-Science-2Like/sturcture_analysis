from TexSoup import TexSoup
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up directory for LaTex Input
directory = "Tex Files"
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
# TODO file input muss robuster werden
logger.info("Load LaTex File into Soup")
# Create Dictionary to store soup objects
soup_dicct = {}
for i,item in enumerate(texfiles):
    soup = TexSoup(open(item))
    logger.debug(soup)
    soup_dicct[i] = soup
logger.debug(soup_dicct)
logger.info("Soup objects successfully loaded into dicctionary.")
logger.info(f"Dicctionary Size: {len(soup_dicct)}")



# Find Elements in LaTex File --------------------
# Load complete Document into "alls"
alls = soup.all
logger.debug(alls)
# for x in range(20):
#     print(alls[x])

logger.info("Find elements in Tex file")
section_list = list(soup.find_all('section'))
# logger.debug(section_list)
# for x in section_list: 
#     print(x)

subsection_list = list(soup.find_all('subsection'))
# logger.debug(subsection_list)
 
abstract = soup.find('abstract')
# logger.debug(abstract)

citations_list = list(soup.find_all('cite'))
# logger.debug(citations_list)
# for x in citations_list:
#     print(x)




