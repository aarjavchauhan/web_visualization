from bs4 import BeautifulSoup
import requests

r = requests.get("https://berobinhood.com/")
soup = BeautifulSoup(r.content, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
