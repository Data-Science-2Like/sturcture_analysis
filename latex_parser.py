from TexSoup import TexSoup
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load File into Soup
# TODO wie parst man über alle Namen der Dokumente drüber??
soup = TexSoup(open("Tex Files\\NeuroCite.tex"))
logger.info("Load Tex File into Soup")
logger.debug(soup.section)
logger.debug(soup)



# Find Elements in LaTex File --------------------

# Load complete Document into "alls"
alls = soup.all
logger.debug(alls)
# for x in range(20):
#     print(alls[x])

logging.info("Find elements in Tex file")
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




