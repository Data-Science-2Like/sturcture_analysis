from ntpath import join
import random
from os import system, name
from typing import Counter
from xxlimited import new
from TexSoup import TexSoup
import logging
import datetime
import re
import csv
import json
import nltk
from nltk.stem import WordNetLemmatizer
from Tree import *
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter



# Set up logging
logging.basicConfig(level=logging.DEBUG, filename="Logs/data_extraction_output.log")
logger = logging.getLogger(__name__)

logger.info("========================================================================")
logger.info("Start logging")
logger.info(datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
# Set up directory for LaTex Input
directory = "Latex"
template_filename = "JSON/templates.json"
csv_filename_16k = "CSV/lemmatizer/sections_16k_lemma_v2.csv"
csv_filename_61k_train = "CSV/sections_headings_61k_train.csv"
csv_filename_61k_test = "CSV/sections_headings_61k_test.csv"
csv_filename_2k = "CSV/lemmatizer/sections_2k_lemma.csv"
csv_filename_improved = "CSV/lemmatizer/sections_improved_lemma.csv"
syn_filename = "JSON/synonyms_origin.json"
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
# ############################################################
#   Variables
# ############################################################
# Create List with Training Documents
D = []
# Create Rule Set
R = []
# Create Synonym Dict
synonyms = {}
# Create List for Nonesense sections
nonsense_list = []
# Create Lemmatizer Object
wordnet_lemmatizer = WordNetLemmatizer()

# ############################################################
#   Methods
# ############################################################
#   Get Data from Documents
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
#   define our clear function
# ############################################################
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# ############################################################
#   Iterate through all Documents
# ############################################################
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

# ############################################################
#   Search for papers with nonsense headings
# ############################################################
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


# ############################################################
#   Write into CSV file
# ############################################################
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


# ############################################################
#   Read from CSV file
# ############################################################
def load_items_from_csv(csv_filename):
    csv_list = []
    # Read out csv file
    with open(csv_filename, 'r') as csvfile:
            # Creating csv writer object
            csvreader = csv.reader(csvfile)

            for item in csvreader:
                csv_list.append(item)
    return csv_list

# ############################################################
#   Load data from JSON file
# ############################################################
def load_from_json_file(filename):
    data = json.load(open(filename, 'r'))
    return data

# ############################################################
#   Lemmatize CSV file
# ############################################################
def lemmatizer(csv_file_in, csv_file_out):
    
    csv_list = []
    # Read out csv file
    with open(csv_file_in, 'r') as csvfile:
            # Creating csv writer object
            csvreader = csv.reader(csvfile)

            for item in csvreader:
                csv_list.append(item)

    new_row = []
    with open(csv_file_out, 'w') as csvfile:
        # Creating csv writer object
        csvwriter = csv.writer(csvfile)

        for item in csv_list:
            #print(item)

            for string in item:
                #print(string)
                if "Latex" not in string:
                    string = string.lower()
                if "appendix" in string:
                    break
                if "appendices" in string:
                    break

                words = nltk.word_tokenize(string)
                stem_sentence = []
                for x in words:
                    stem_sentence.append(wordnet_lemmatizer.lemmatize(x))
                    stem_sentence.append(" ")
                string = "".join(stem_sentence).rstrip()
                new_row.append(string)
            csvwriter.writerow(new_row)
            new_row = []


# ############################################################
#   Calculate Support
# ############################################################
def support_method(anzahl_dict, anzahl_regel, anzahl_gesamt):
    percentage = 0
    percentage = anzahl_dict[anzahl_regel] / anzahl_gesamt
    return round(percentage, 4)
    # str_per = '%.8f' % percentage
    # logger.debug(f"Percentage Rule {str_per} : {rule}")
    #return percentage


# ############################################################
#   Test how many Paper match the templates
# ############################################################
def test_templates(templates, csv_list, synonyms):
    counter = 0
    fail_counter = 0
    tree = Tree(["*"], None)
    temp_set = set()
    csv_set = set()

    # Convert template list to Set
    for item in templates:
        temp_set.add(tuple(item))
    
    # Convert HS list to Set
    for item in csv_list:
        csv_set.add(tuple(item[1:]))

    # Create Template Tree
    for templ in temp_set:
        if templ:
            update_tree(tree, templ)
    
    # Update Template Tree with new headings
    for templ in csv_set:
        if templ:
            update_tree(tree, templ)

    # Export as anytree
    atree = t2anytree(tree)

    # Prune tree 
    root = atree.children[0]
    root.parent = None
    # Count Nodes
    counter = sum([1 for node in PreOrderIter(root)])
    fail_counter = sum([1 for node in PreOrderIter(atree)])

    # graphviz needs to be installed for the next line!, #N: via apt, not pip
    DotExporter(root).to_picture("pictures/test_tree.png")

    print("_________________________")
    print("Number of Papers: ", len(csv_list))
    print("Size of Template Batch: ", len(templates))
    print("Size of Tree: ", counter)
    print("Number of Papers that matched Template: ", (len(csv_list) - fail_counter + 1))
    print("Number of Papers not matched: ", fail_counter-1)

    return root



# ############################################################
#   Main Loop
# ############################################################
def loop(templates, csv_list):
    print("================================================================")
    print("================== Structured Data Extraction ==================")
    print("================================================================")
    train = []
    tree = Tree(["*"], None)
    temp_set = set()
    add_set = set()
    support_dict = {}
    hit_counter = 0
    
    # Choose size of training set
    for i in range(500):
        train.append(random.choice(csv_list))


    print(f"Size of Corpus: {len(csv_list)}")
    print(f"Size of Training Set: {len(train)}")

    ## Create Tree with Templates
    # Convert template list to Set
    # Create dict to hold support values
    for item in templates:
        temp_set.add(tuple(item))
        new_template_tup = tuple(item)
        # 2 Counter (# matches, # multimatches)
        support_dict[str(new_template_tup)] = [0, 0] 
    
    support_dict["['*']"] = [0, 0]
    # for itrm in support_dict:
    #     print(itrm)

    # Create Template Tree
    for templ in temp_set:
        #print(type(templ))
        #print(templ)
        if templ:
            update_tree(tree, templ)
        
    
    # Export as anytree
    atree = t2anytree(tree)
    #print(RenderTree(atree))
    ##
    counter = 0
    r = []
    # Iterate through alle docs
    for i, docs in enumerate(train):
        
        for items in docs:
            ###
            # If Latex in name or empty => skip 
            if "Latex" in items:
                continue
            if len(items) == 0:
                continue
            if "appendix" in items:
                break
            ##

            ## Synonym Dict swap 
            # Check if Section Heading already in Synonyms
            for i, syn in enumerate(synonyms):
                # If SH is  in Synonyms => replace with synonym
                if items == syn:
                    #print(i, ":" ,items)
                    items = synonyms[syn]
                    #print(i, ":" ,items)

            # Add section heading to list
            r.append(items)
            # If section is "conclusion" cut everything after it
            if "conclusion" in items:
                break 
            ##
        ## 
        # Remove Duplicates
        #print(f"r: {r}")
        r = list(dict.fromkeys(r))
        ##

        ## Loop
        # 
        counter += 1
        running = True
        while(running):
            # Clear screen and print Tree
            
            clear()
            # for pre, _, node in RenderTree(atree):
            #     print("%s%s" % (pre, node.name))
            # print("_______________________________________________________________________________")
            print(counter)
            # Declare root of tree
            root = atree.root
            #root = atree.children[0]
            new_rule_tup = tuple(r)
            if len(new_rule_tup) < 1:
                continue

            ##
            # iterate through tree 
            for item in PreOrderIter(root):
                res = eval(item.name)
                
                if sub(new_rule_tup, res):
                    print("Rule found in templates.")
                    print(f"Template: {res}")
                    support_dict[str(res)][0] += 1                                 


            # print("_______________________________________________________________________________")
            # print(f"Rule: {r}")
            # print(f"Counter: {counter}")
            # ##

            # # Get User Input
            # user_input = input("Do you want to add a new rule? (Press [r])\nDo you want to add a synonym? (Press [s])\nFor the next rule: (Press [n])\n")
            # if user_input == "r":
            #     print("Rule added.")
            #     # Convert Rule to Tuple > insert into Tree
            #     add_set.add(tuple(r))
            #     for item in add_set:
            #         update_tree(tree, item)
            #     # Export as anytree
            #     atree = t2anytree(tree)
            #     r = []
            #     running = False
            # elif user_input == "s":
            #     print("introduction | related work | method | experiment | discussion | conclusion | \n")
            #     sec_input = input("Please enter the section you want to add an synonym to:\n")
            #     syn_input = input("Please enter the synonym:\n")
            #     synonyms[syn_input] = sec_input
            # elif user_input == "n":
            #     r = []
            #     running = False
            r = []
            running = False
        ##

    clear()
    for pre, _, node in RenderTree(atree):
        print("%s%s" % (pre, node.name))
        
    # Prune tree 
    root = atree.children[0]
    root.parent = None
    # Count Nodes
    counter = sum([1 for node in PreOrderIter(root)])
        
    # Statistics     
    print("_______________________________________________________________________________")
    print("Number of Papers: ", len(csv_list))
    print("Size of Training Batch: ", len(train))
    print("Size of Template Batch: ", len(templates))
    for item in support_dict:
        try:

            support = round( (support_dict[item][0] )/ (len(train)) ,2)
        except ZeroDivisionError:
            support = 0
        if support > 0:
            print(f"{item}: {support}")
        #print(f"{item}: {(support_dict[item][0] + support_dict[item][1] )/ len(train)}")
        #print(f"{item}: {support_dict[item]}")

        


# ############################################################
#   Main Function Calls
# ############################################################
#load_items_into_soup()
#load_into_csv_file()
# iter_through_doc_set()
#find_nonsense_paper()

# Loading Lists from external Documents
csv_61k_train = load_items_from_csv(csv_filename_61k_train)
csv_61k_test = load_items_from_csv(csv_filename_61k_test)
csv_16k = load_items_from_csv(csv_filename_16k)
csv_improved = load_items_from_csv(csv_filename_improved)
csv_2k = load_items_from_csv(csv_filename_2k)
synonyms = load_from_json_file(syn_filename)
templates = load_from_json_file(template_filename)

#test_templates(templates, csv_improved, synonyms)    # Wie viele Paper matchen?
loop(templates, csv_61k_train)

# file_in = "CSV/sections_headings_61k_test.csv"
# file_out = "CSV/sections_headings_61k_test.csv"
# lemmatizer(file_in, file_out)


# ############################################################
#   Write data to output files
# ############################################################
json_data = json.dumps(R, indent = 4)
synonym_data = json.dumps(synonyms, indent = 4)
with open("JSON/rules.json", "w") as outfile:
   outfile.write(json_data)
with open("JSON/synonyms.json", "w") as outfile:
    outfile.write(synonym_data)
