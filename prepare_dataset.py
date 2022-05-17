from TexSoup import TexSoup
import multiprocessing as mp
import os
import datetime
import logging
import csv
import re


# ############################################################
#   Write into CSV file
# ############################################################
def load_into_csv_file(item):
    new_section_list = []
    try:
        #logger.debug(f"Load {i}: {item} into soup.")
        soup = TexSoup(open(item), tolerance=1)

        new_section_list.append(item)
                
        section_list = list(soup.find_all('section'))
                
        for item in section_list:
            clean_string = re.sub('[^A-Za-z0-9 ]+', '', item.string)
            # In case of "uppercaseIntroduction"
            if "uppercase" in clean_string:
                clean_string = clean_string.split("uppercase")[1]
            # Go through token_list, bc parser falsely sets them as sections    
            if [ele for ele in token_list if(ele in clean_string)]:
                continue
            new_section_list.append(clean_string)

    except Exception as e:
        #logger.debug(f"Doc #{i}: {item} could not be loaded.")
        logger.debug("Error occured: "+ str(e))

    return new_section_list


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, filename="Logs/dataset_output.log")
    logger = logging.getLogger(__name__)

    directory = "Latex_files/full/expanded"
    
    token_list = ["0pt", "8pt", "Abstract", "startsectionsection1z", "Credits", "cntformat", "1", "2", "3"]
    texfiles = []

    logger.info("========================================================================")
    logger.info("Start logging")
    start_time = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
    logger.info(start_time)


    # Create Rule Set
    R = []
    pool = mp.Pool(mp.cpu_count())

    # Iterate over files in directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Checking if it is a file
        if os.path.isfile(f):
            texfiles.append(f)

    # Cut down to 5
    texfiles = texfiles[8150:]

    # Load File into Soup
    logger.info("Load LaTex File into Soup")

    result_list = []


    # Function Calls
    result = pool.map(load_into_csv_file, [item for item in texfiles])

    result_list = []
    for item in result:
        if len(item) > 0:
            result_list.append(item)

    #print(result_list)


    pool.close()

    filename = "CSV/Remote/sections_headings_remote_part_2.csv"
    with open(filename, 'w') as csvfile:
        # Creating csv writer object
        csvwriter = csv.writer(csvfile)

        for item in result_list:
            #logger.debug(f"Append {item} to File.")
            csvwriter.writerow(item)
            #csvfile.flush()
       
    
    logger.info("========================================================================")
    logger.info("End logging")
    end_time = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
    logger.info(end_time)
