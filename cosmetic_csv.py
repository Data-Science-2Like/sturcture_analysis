import csv
import logging

in_filename = "/home/danial/Documents/GitHub/latex_parser/CSV/Remote/sections_headings_remote_part_final.csv"
out_filename = "/home/danial/Documents/GitHub/latex_parser/CSV/Cosmetic/sections_headings_61k_cosmetic.csv"
new_list = []

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/cosmetic_output.log")
logger = logging.getLogger(__name__)


# Read out csv file
with open(in_filename, 'r') as csvfile:
        # Creating csv writer object
        csvreader = csv.reader(csvfile)

        section_list = []

        for item in csvreader:
            section_list.append(item)


with open(out_filename, 'w') as csvfile:
    # Creating csv writer object
    csvwriter = csv.writer(csvfile)

    for list in section_list:
        #print(len(list))
        if len(list) < 2:
            continue
        for item in list:
            # print(item)
            if len(item) > 0:
                new_list.append(item)

        # writing the fields
        logger.debug(f"Append | {new_list}  | to File.")
        csvwriter.writerow(new_list)
        new_list = []