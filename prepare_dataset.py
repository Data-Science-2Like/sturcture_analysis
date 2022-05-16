from TexSoup import TexSoup
import os
import datetime
import logging
import csv
import re



# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/dataset_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))

directory = "Latex_files/full/expanded"
texfiles = []
# Create List with Training Documents
D = []
# Create Rule Set
R = []

# Iterate over files in directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # Checking if it is a file
    if os.path.isfile(f):
        texfiles.append(f)

# Cut down to 5
texfiles = texfiles[:20]

# Load File into Soup
logger.info("Load LaTex File into Soup")

# ############################################################
def load_items_into_soup():
    for i,item in enumerate(texfiles):
        try:
            logger.debug(f"Load {i}: {item} into soup.")
            soup = TexSoup(open(item), tolerance=1)
            D.append(soup)

        except Exception as e:
            logger.debug(f"Doc #{i}: {item} could not be loaded.")
            logger.debug("Error occured: "+ str(e))

# ############################################################
#   Write into CSV file
# ############################################################
def load_into_csv_file():
    filename = "CSV/Remote/sections_headings_remote.csv"

    with open(filename, 'w') as csvfile:
        # Creating csv writer object
        csvwriter = csv.writer(csvfile)
        token_list = ["0pt", "8pt", "Abstract", "startsectionsection1z", "Credits", "cntformat", "1", "2", "3"]

        for i,item in enumerate(texfiles):
            try:
                new_section_list = []
                # Logging if file can't load
                logger.debug(f"Load {i}: {item} into soup.")
                # Parsing TeXfile to soup, tolerance=1 for better section detection [errors with math mode]
                soup = TexSoup(open(item), tolerance=1)
                # Find all sections and add to list
                section_list = list(soup.find_all('section'))
                new_section_list.append(item)

                # Iterate through sections to get rid of errors 
                for item in section_list:
                    item = item.lower()

                    clean_string = re.sub('[^A-Za-z0-9 ]+', '', item.string)
                    # In case of "uppercaseIntroduction"
                    if "uppercase" in clean_string:
                        clean_string = clean_string.split("uppercase")[1]
                    # Go through token_list, bc parser falsely sets them as sections    
                    if [ele for ele in token_list if(ele in clean_string)]:
                        continue

                    new_section_list.append(clean_string)
                
                # writing the fields
                logger.debug(f"Append | {new_section_list}  | to File.")
                csvwriter.writerow(new_section_list)

            except Exception as e:
                logger.debug(f"Doc #{i}: {item} could not be loaded.")
                logger.debug("Error occured: "+ str(e))


# Function Calls
load_items_into_soup()
load_into_csv_file()
