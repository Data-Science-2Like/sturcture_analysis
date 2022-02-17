import random
from TexSoup import TexSoup
import logging
import os
import datetime
import re
import csv
import json
import nltk
from nltk.stem import WordNetLemmatizer



# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/data_extraction_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
# Set up directory for LaTex Input
directory = "Latex"
csv_filename = "CSV/sections_headings.csv"
texfiles = []


# logger.info("Append LaTex Files to List")
# # Iterate over files in directory
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     # Checking if it is a file
#     if os.path.isfile(f):
#         logger.debug(f)
#         texfiles.append(f)

# Load File into Soup
logger.info("Load LaTex File into Soup")

# Create List with Training Documents
D = []
# Create Rule Set
R = []
# Create Synonym Dict
synonyms = {
    "Introduction" : [],
    "Related Work" : [],
    "Methods" : [],
    "Experiments" : [],
    "Result" : [],
    "Discussion" : [],
    "Conclusion" : [],
    "Future Work" : []
}
# Create List for Nonesense sections
nonsense_list = []
# Create Lemmatizer Object
wordnet_lemmatizer = WordNetLemmatizer()

def load_items_into_soup():
    for i,item in enumerate(texfiles):
        try:
            logger.debug(f"Load {i}: {item} into soup.")
            soup = TexSoup(open(item), tolerance=1)
            D.append(soup)

        except Exception as e:
            logger.debug(f"Doc #{i}: {item} could not be loaded.")
            logger.debug("Error occured: "+ str(e))

def load_into_csv_file():
    filename = "CSV/sections_headings_16k.csv"

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

def load_items_from_csv():
    # Read out csv file
    with open(csv_filename, 'r') as csvfile:
            # Creating csv writer object
            csvreader = csv.reader(csvfile)

            for item in csvreader:
                D.append(item)
            

def find_nonsense_paper():
    for i, item in enumerate(D):
        section_list = list(item.find_all('section'))
        logger.debug(str(i))
        new_section_list = []
        for item in section_list:
            clean_string = re.sub('[^A-Za-z0-9 ]+', '', item.string)
            new_section_list.append(clean_string)
        if new_section_list:
            if not new_section_list[0] == "Introduction":
                nonsense_list.append(new_section_list)

        logger.debug(new_section_list)
        # try:
        #     if new_section_list[1] == "Introduction":
        #             logger.debug(new_section_list[1])
        # except Exception as e:
        #     logger.debug(f"Doc #{i}: {item} could not be loaded: {e}.")
        logger.debug("==================================================================")


def support_method(rule):
    percentage = 0
    sections = []
    for docs in D:
        for items in docs:
            if "Latex" in items:
                continue
            if len(items) == 0:
                continue
            # String completly lowercase
            item = items.lower()  

            words = nltk.word_tokenize(item)
            stem_sentence = []
            for x in words:
                stem_sentence.append(wordnet_lemmatizer.lemmatize(x))
                stem_sentence.append(" ")
            item = "".join(stem_sentence).rstrip()

            sections.append(item)
        if rule == sections:
            percentage += 1
        sections = []
    percentage = percentage / len(D)
    return round(percentage, 4)
    # str_per = '%.8f' % percentage
    # logger.debug(f"Percentage Rule {str_per} : {rule}")
    #return percentage

def iter_through_doc_set():
    # loop until D is empty
    logger.debug("Size of Corpus : {}".format(len(D)))
    r = []
    for docs in D:
        for items in docs:
            if "Latex" in items:
                continue
            if len(items) == 0:
                continue
            
            # String completly lowercase
            item = items.lower()    

            # Stemming the Sections to reduce redudancy
            words = nltk.word_tokenize(item)
            stem_sentence = []
            for x in words:
                stem_sentence.append(wordnet_lemmatizer.lemmatize(x))
                stem_sentence.append(" ")
            item = "".join(stem_sentence).rstrip()
            
            r.append(item)

        r.append(support_method(r))
        #print(support_method(r))
        if r in R:
            r = []
            continue
        # TODO UserInput when to add rule
        # TODO When to add rule >> support % ??
        R.append(r)
        r = []        

    logger.debug("Size of Rule Set : {}".format(len(R)))
    logger.debug("Complete Rule Set: {}".format(R))


# Alles nach Appendix wegwerfen                         X
# Support Methode > auf wie viele Paper matched es      X
# Abweichung bei Regeln zulassen (1 Sektion)
# TODO Synonymliste                                     X
# ersten 100 dokumente anschauen                        X
# mehrere Mögichkeiten:
#   - Wörterbuch hinzufügen
#   - Regel hinzufügen
# Läuft dann auto über die restlichen Dokumente 
# Test über die restlichen Dokumente
# DSR
# Wörterbuch und Regel in Dateien speichern             X
# Wörterbuch während der Laufzeit definieren 
# >> alles Begriffe die das gleiche Bedeuten 
# Sections mit "and" verbunden als neue Regel 
# Matching mit Regex über String (* Wildcard)
# Wildcard >> Literatur suchen 


def loop():
    print("================================================================")
    print("================== Structured Data Extraction ==================")
    print("================================================================")
    train = []
    running = True

    for i in range(10):
        train.append(random.choice(D))

    while(running):
        # Load the Corpus
        print(f"Size of Corpus: {len(D)}")
        print(f"Size of Training Set: {len(train)}")
        
        r = []
        for docs in train:
            for i,items in enumerate(docs):
                if "Latex" in items:
                    continue
                if len(items) == 0:
                    continue
                
                
                # String completly lowercase
                item = items.lower()    

                # Stemming the Sections to reduce redudancy
                words = nltk.word_tokenize(item)
                stem_sentence = []
                for x in words:
                    stem_sentence.append(wordnet_lemmatizer.lemmatize(x))
                    stem_sentence.append(" ")
                item = "".join(stem_sentence).rstrip()
 
 
                # try:
                #     # Add to Rule and Synonyms
                #     if not item in synonyms[i]:
                #         synonyms[i].append(item)
                # except Exception as e:
                #     print("Index out of range: ",e)
                #     break
 
 
                r.append(item)
                # If section is "conclusion" cut everything after it
                if "conclusion" in item:
                    break                

            r.append(support_method(r))
            #print(support_method(r))
            if r in R:
                print(f"Rule {r} already in Ruleset.")
                r = []
                continue
            print(f"New Rule: {r}")
            print(f"No matching Rule found.")
            user_input = input("Do you want to accept new rule? (Press [r])\n Do you want to add a synonym? (Press [s]\n")
            if user_input == "r":
                R.append(r)
                r = []
            elif user_input == "s":
                user_input = input("Please enter the index:\n")
                synonyms[user_input]
            else:
                r = []


        if input("Quit the script?\n") == "y" or input("Quit the script?\n") == "yes":
            running = False
            


        


# Main function calls ===================================================
#load_items_into_soup()
#load_into_csv_file()
load_items_from_csv()
#iter_through_doc_set()
loop()
#find_nonsense_paper()


# Write Sections to JSON File
json_data = json.dumps(R, indent = 4)
synonym_data = json.dumps(synonyms, indent = 4)
with open("JSON/rules.json", "w") as outfile:
   outfile.write(json_data)
with open("JSON/synonyms.json", "w") as outfile:
    outfile.write(synonym_data)