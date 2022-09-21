# Structure Analysis

To provide our pipeline with information on each section, we perform a structural analysis. 
Sites we arXiv provide datasets which consist of latex documents. 
We iterate these datasets with the tool TexSoup (https://github.com/alvinwan/TexSoup)  to extract the necessary information.
In this case we mainly restrict ourselves to the section titles. 

All section titles of a document form a sequence. 
We sort these sequences into a template tree we have designed.
Then we calculate the support values for each sequence.

We also defined a synonym dictionary that divides section titles into 7 categories:
- Introduction
- Related Work
- Method
- Experiment
- Result
- Discussion
- Conclusion

While sorting into the tree we compare the titles with the entries in the dictionary and replace them if they fall into one of the 7 categories. 

## Preprocessing

With "latex_parser.py" we load the dataset from arXiv into the soup objects from TexSoup and extract the section headings. At this step we already sort out some cases, where no useful section headings can be extracted. 
The latex dataset is contained in the folder "Latex files".
We then safe the section headings into a JSON file. All JSON files are contained in the "JSON" folder.
As the next step we use "cosmetic.py" and which uses a lemmatizer and some filters on our section headings.
We save the processed section headings into a CSV file. All CSV files are contained in the "CSV" folder.

## Synonym Dictionary + Duplicate Removal + Template Matching

Our main programm is in the "structured_data_extraction.py" file. We define our functionality for the active wrapper approach here and for our synonym dictionary. To use our program some files need to be loaded:
- JSON/synonyms_origin.json (Synonym Dictionary)
- JSON/templates.json (Template Tree)
- CSV/sections_headings_61k_train.csv (Train Data Set)
- CSV/sections_headings_61k_test.csv (Test Data Set)

With these files supplied the synonym dictionary and the duplicate removal work automatically. 
While matching the templates, the user has the option to add synonyms to the dictionary. 

In the file "Tree.py" we describe the functionality for our template tree. 

## Misc

We created some statistics while performing our experiments. All code herefor is in "create_statistics.py".

## Usage
python3 prepare_dataset.py
This file will convert the dataset from tex files to a csv file. 
The input directory can be specified at line 47.
The output file can be specified at line 93.

python3 create_statistics.py
This file was used to create statistics about the dataset.
In line 6 the input file needs to be specified. 
It will then automatically create the statistics and save it to the folder "/pictures".

python3 cosmetic_csv.py
This file needs the input and output file specified in line 4 and 5.
It will automatically remove empty and too short entries. 

python3 structured_data_extraction.py
This file needs as input the dataset (line 29-31), the synonym dictionary (line 34) and the templates (line 28).
The output files can be specified in line 526 and 528.
This starts the main loop. The tree will be built and the rules gathered from the data set will be iterated. 
Press "s" to add a synonym to the dictionary.
Press "n" to advance to the next rule. 
After all rules were iterated the results will be presented.
