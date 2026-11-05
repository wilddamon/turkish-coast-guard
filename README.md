Scripts to download and compile daily activity reports from the Turkish Coast Guard website.

Scripts were run in the following order:

1.) scrape.py -> looks for reports including one or two days of data, and downloaded the html files.


2.) combine_results.py -> assembles the data from the html files (number of rescues stated on the web page and link to the rescue docx file) into a spreadsheet, which can then be inspected to find missing records. A column named "missing" should be added manually.


3.) I noticed that some records were across three days, so I added scrape_threes.py. It looks for missing days in the spreadsheet and attempts to download the html for spans of three days. combine_results.py should then be again.


4.) download_docx.py -> iterates through the spreadsheet and downloads the docx files.


5.) extract_docx.py -> reads all the docx files, and combines the data into a spreadsheet. country_aliases.py is a helper file where I recorded all the odd spellings of countries that I found.
