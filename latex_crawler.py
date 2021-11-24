from TexSoup import TexSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load File into Soup
soup = TexSoup(open("Tex Files\\acl2021.tex"))
logger.info("Load Tex File into Soup")
logger.debug(soup.section)
#logger.debug(soup)

# Find Elements in LaTex File
logging.info("Find elements in Tex file")
section_list = list(soup.find_all('section'))
logger.debug(section_list)

subsection_list = list(soup.find_all('subsection'))
logger.debug(subsection_list)

abstract = soup.find('abstract')
logger.debug(abstract)

citations_list = list(soup.find_all('cite'))
logger.debug(citations_list)