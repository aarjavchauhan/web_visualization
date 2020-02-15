from bs4 import BeautifulSoup
import requests
import re

listOfHistory = []

file = open("links.txt", "rt")
while True:
    # Get next line from file
    line = file.readline()
    # If line is empty then end of file reached
    if not line:
        break
    regexMatch = re.match("(http://|ftp://|https://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", line)
    if bool(regexMatch):
        listOfHistory.append(regexMatch.groups())
file.close()

for item in listOfHistory:
    soup = BeautifulSoup(requests.get(item[0]+item[1]+item[2]).content, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))
    # # optimize code for internal and external links, should i categorize on each type?
        # print(link.get('href')

# r = requests.get(listOfHistory[0][0]+listOfHistory[0][1])
# soup = BeautifulSoup(r.content, 'html.parser')

# networkDict = {}

# for link in soup.find_all('a'):
# # optimize code for internal and external links, should i categorize on each type?
#     print(link.get('href'))
