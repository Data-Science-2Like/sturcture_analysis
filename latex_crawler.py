from TexSoup import TexSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


soup = TexSoup(open("Tex Files\\acl2021.tex"))
logger.info("Load Tex File into Soup")

