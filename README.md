This repo contains some of useful scripts I made.

Usage instructions:

# 1. Hotstar downloader:
Install dependencies - python3, ffmpeg and youtube-dl. Create a file with links to be downloaded on each new line. Run the program using:
'''
python3 downloader.py my-file-with-links.extension
'''
If it spews "Requested format is not available", change "hls-861" in downloader.py to one of the output of this:
'''
youtube-dl -F https://www.hotstar.com/sample-link-that-failed
'''

# 2. SPPU result scraper
Install dependencies - python3 and selenium. Download [chrome webdriver] (https://sites.google.com/a/chromium.org/chromedriver/downloads) and edit SppuResultScraper.py 11th line to include path of chromedriver. Edit pdf2info.py according to pdf/data of college records. The scripts should return a 2d matrix of Seat Number and Mother's Name. 

First run pdf2info.py:
'''
python3 pdf2info.py --input=/path/to/your.pdf
'''
It should create a new file "student\_info.p". Then execute the scripts:
'''
python3 SppuResultScraper.py
'''
It should create couple of files with SGPA List.csv being file of interest.

