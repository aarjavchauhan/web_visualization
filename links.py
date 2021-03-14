from bs4 import BeautifulSoup
import requests
import re
import os
from urllib.parse import urlparse, urljoin
import validators
import json

# list storing URLs from a file
urls_from_file = []
# list of URLs which have yet to crawled through
urls_to_process = []
# set of URL which have been already processed
urls_already_processed = set()
# list storing dictionaries of relationships
relationships = []

"""
Helps read files, especially on windows
returns a python readable file location
"""
def find_file():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(THIS_FOLDER, 'data1.json')
    return file_name

"""
Takes a url and runs it through a validator
"""
def parse_url(url):
    try:
        if(not bool(validators.url(url))):
            return None
    except TypeError:
        return None
    return url

"""
Takes a file name ,reads the file and parses every line.
Ensures link is valid.
"""
def read_file(file_name):
    with open(file_name) as file:
        for line in file:
            parsed_url = parse_url(line.strip())
            if(parsed_url):
                urls_from_file.append(parsed_url)

def read_file_json(file_name):
    with open(file_name) as file:
        data = file.read()
        pretty_json = json.loads(data)
        for struct in pretty_json:
            parsed_url = parse_url(struct["url"])
            if parsed_url:
                urls_from_file.append(parsed_url)

"""
Gets all the links on a webpage
"""
def get_links(url_list, layer):
    hrefs = []
    url_layer = []
    for url in url_list:
        try:
            if(validators.url(url)):
                soup = BeautifulSoup(requests.get(url, timeout=20).content, 'lxml')
                hrefs = soup.find_all('a')
                url_layer = url_layer + establish_relationships(url, hrefs, layer)
        except TypeError:
            print(TypeError)
            continue
        except ConnectionError:
            print(ConnectionError)
            continue
        except TimeoutError:
            print(TimeoutError)
            continue
        except Exception as e:
            print(e)
            continue
    urls_to_process.append(url_layer)

"""
Takes a from url and a set of hrefs that are related to it,
Saves the relationship using a dict in a list.
"""
def establish_relationships(source_url, hrefs, layer):
    destination_urls = []
    for item in hrefs:
        link = item.get('href')
        # print(source_url)
        # print(link)
        broken_down_link = parse_url(link)
        if(broken_down_link and (broken_down_link not in urls_to_process) and (broken_down_link not in urls_already_processed) and (broken_down_link != source_url)):
            # print(link + "---"+ broken_down_link)
            if(check_manual_URL_rules(broken_down_link)):
                destination_urls.append(broken_down_link)
            relationships.append({'from':source_url, 'to':broken_down_link, 'layer':layer})
            print(layer)
    urls_already_processed.add(source_url)
    return destination_urls

"""
Function which includes manual rules for validations
"""
def check_manual_URL_rules(link):
    blacklist = ['spotify', 'boulderoem']
    hostname = urlparse(link).netloc.split('.')
    if(not any(item in hostname for item in blacklist)):
        return True
    return False

"""
function which returns second level domain
"""
def get_second_level_domain(link):
    second_level_domain = urlparse(link).netloc.split('.')[-1:].pop()
    return second_level_domain

"""
Main function
"""
def main():
    #constant that represents how many links in urls_to_process
    #should be processed
    NUMBER_OF_LAYERS_TO_PROCESS = 2

    #Establish file location, read and parse file
    file_name = find_file()
    ##read_file(file_name)
    read_file_json(file_name)

    #Get initial links and establish relationships
    #of links from file
    get_links(urls_from_file, 0)

    #Loop over urls in queue, and get their links and
    #establish their relationships

    for layer in range(0,NUMBER_OF_LAYERS_TO_PROCESS):
        if(len(urls_to_process) != 0):
            get_links(urls_to_process.pop(0), layer+1)
        else:
            break

    # print('printing urls already processed!!!!')
    # print(urls_already_processed)
    # print('printing urls already processed!!!!')


    with open('results.json', 'w') as f:
        json.dump(relationships, f)


if __name__== "__main__":
  main()
  urls_already_processed_list = list(urls_already_processed)
  edges = []

  no_dup_relationships = [dict(s) for s in set(frozenset(d.items()) for d in relationships)]

  for entry in no_dup_relationships:
    try:
        edges.append({'source': urls_already_processed_list.index(entry.get('from')), 'target': urls_already_processed_list.index(entry.get('to')), 'layer':entry.get('layer')})
    except Exception as e:
        # print(e)
        continue

  nodes = [{'name': s, 'secondLevelDomain': get_second_level_domain(s)} for s in urls_already_processed_list ]

  dataset = {'nodes': nodes, 'edges': edges }

  print('\n\n\nPrinting Dataset \n\n\n')
  print(dataset)

  with open('results.json', 'w') as f:
     json.dump(dataset, f)
