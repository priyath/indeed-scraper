# Steps to configure and execute the tool

Important: The script requires python3 for successful execution

installing python3 for Ubuntu:
http://docs.python-guide.org/en/latest/starting/install3/linux/

installing python3 for MAC: 
http://docs.python-guide.org/en/latest/starting/install3/osx/

## DEPENDENCIES (execute the provided commands in the terminal)

1. html parsing utility 
to install: `pip3 install -U beautifulsoup4`

2. selenium 
to  install: `pip3 install -U selenium`

3. Download the appropriate chromedriver version for selenium from 
https://chromedriver.storage.googleapis.com/index.html?path=2.35/

unzip the downloaded zip file and copy the 'chromedriver' file to any location. Note down the path. Update
indeed.py script with the path to the 'chromedriver' file at:

`browser = webdriver.Chrome(executable_path="/path/to/chromedriver")`

## EXECUTION

The script can be executed from the command line like so:

`python3 indeed.py "keyword" "Country" "City(optional)"`

refer `indeed.py` domain mapping to see the set of supported countries. If a City is not specified as an argument, the search
will be done for the whole country.

## OUTPUT

The company,location tuple will be saved to a csv file upon execution. The csv file will be named as: keyword_country.csv

