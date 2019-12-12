# author @susanemcg
# This file is not updated for Python3

import urllib2
from bs4 import BeautifulSoup

# Program outline:
#
# 1. Loop through lines in source file, each of which contains a unique id and a street address somewhere in Miami
# 2. Search website and temporarily download resulting HTML page (overwritten each time)
# 3. If parsed page contains valid info, write unique id, address and zip code to output file

baseURL = "http://www.whitepages.com/search/FindNearby?utf8=%E2%9C%93&street="

urlSuffix ="&where=Miami%2C+FL"

sourceFile = open("Unresolved_w_ID.csv", "rU")


# Change the name of the output file every time the script below breaks and needs to be restarted
# That way, can compare address returned to what's in source file by lining up unique ids

# create unique, writable output file

outputFile = open("Resolved_w_ID1.csv", "w")


# python (2) doesn't support different starting points for loops, even when an explicit iterator
# has been defined through *enumerate*
for i, line in enumerate(sourceFile):

# Because of this, we have to manually change *i* to reflect last successfully parsed address (e.g. 1470)
# This avoids unnecessary searches, without missing any data

	if i > 1470:
		# split the line on commas
		line_list = line.split(",")
		# unique id is first element
		unique_id = line_list[0]
		# address is 22nd element
		address_part = line_list[21]
		# format address for query
		address_format = "+".join(address_part.split())
		# open webpage and read data
		webpage = urllib2.urlopen(baseURL+address_format+urlSuffix)
		webdata = webpage.read()
		# note that every time I download the results page, it overwrites; we don't
		# want/need to store the results
		localFile = open("TempFile.html", "w")
		localFile.write(webdata)
		localFile.close()
		webpage.close()
		# open the temporary copy of the webpage, BeautifulSoup command parses the HTML
		pageSoup = BeautifulSoup(open("TempFile.html"))
		# locate the span tag with the address info supplied
		address_confirm = pageSoup.find("span", class_="name block")
		city_zip = pageSoup.find("span", class_="subtitle")
		# if results (e.g. address and zip code) are BOTH present
		if(address_confirm != None and city_zip != None):
			# output the unique item id and the loop id to the terminal, so the
			# most recent successfully entered
			print "At ID = "+str(unique_id)
			print "At line = "+str(i)
			address_plain = address_confirm.get_text(strip=True)
			city_plain = city_zip.get_text(strip=True)
			# write just the unique id, address and zip code to our output file
			outputFile.write(unique_id+","+address_plain+","+city_plain+"\n")

		# don't want to do too many at once, so break at line number shown below
		if i > 4999:
			break

sourceFile.close()
outputFile.close()
