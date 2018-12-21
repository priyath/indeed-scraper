from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import csv

#domain mapping
domains = {
"United States":"https://www.indeed.com/", 
"United Kingdom":"https://www.indeed.co.uk/", 
"Germany":"https://de.indeed.com/", 
"India":"https://www.indeed.co.in/"
}

#parse input arguments
argLength = len(sys.argv)
if (argLength > 4) or (argLength < 2):
	print("Invalid arguments. Expected: \npython3 indeed.py \"keyword\" \"domain\" \"location(optional)\"")
	sys.exit()

keyword = sys.argv[1]
domain = sys.argv[2]
location = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]

#Path to chromedriver. this is required
browser = webdriver.Chrome(executable_path="/home/priyathg/chromedriver")

#build url to scrape
baseUrl = (domains[domain] + "jobs?q=" + keyword + "&l=" + location + "&filter=0&start=").replace(" ", "+");

#get the number of iterations required to iterate the complete result set
def getIterationLimit( searchCount ):
	countArray = searchCount.split()
	if domain == "United States":
		resultCount =int(countArray[3].replace(',', ''))
	else:
		resultCount =int(countArray[5].replace(',', ''))
	if resultCount > 1000:
		return 1000
	return resultCount + (10 - (resultCount % 10))

#find number of iterations required
print("Calculating iterations required based on result count..")
url = baseUrl + str(0)
browser.get(url)
innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
soup = BeautifulSoup(innerHTML, "html5lib")
searchCount = soup.find('div', attrs={'id': 'searchCount'})
limit = getIterationLimit(searchCount.getText())
print(str(limit) + " jobs in " + str(int(limit/10)) + " pages")

outputFilename = (keyword + "_" + location).replace(" ", "_")
with open(outputFilename+'.csv', 'w') as file:
	writer = csv.writer(file, lineterminator = '\n',)
	writer.writerow(["Company","Location"])
	#iterate pages and extract info
	for x in range(0, limit, 10):
		print("parsing page " + str(int((x/10) + 1)) + "/" + str(int(limit/10)))
		url = baseUrl + str(x)
		
		browser.get(url) #navigate to page
		innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string

		soup = BeautifulSoup(innerHTML, "html5lib")

		results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
		shouldTerminate = soup.find('p', attrs={'class': 'dupetext'})

		for x in results:
			title = x.find('a', attrs={"data-tn-element":"jobTitle"})
			company = x.find('span', attrs={"class":"company"})
			location = x.find('span', attrs={"class":"location"})
			writer.writerow([company.getText().strip().rstrip(),location.getText().strip().rstrip()])

		if shouldTerminate != None:
			break

