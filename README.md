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

