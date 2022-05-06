# wier_dn2

The following modules must be installed: bs4, Levenshtein, lxml

Extraction is initiated by running run-extraction.py with A, B or C as parameter
  
The method parameter sets the method of data extraction:

    A - Regex
    
    B - xPath
    
    C - RoadRunner

## Repo organization

__results__ - contains extracted data, each method has its own folder

__webpages__ - contains pages for extraction

__run-extraction.py__ - main script, initializes selected extraction script

__RegexFile.py__ - regex extraction script

__xPathFile.py__ - xpath extraction script

__RoadRunner.py__ - roadrunner extraction script
