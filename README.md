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