import sys
import json
from urllib.parse import urlparse, urljoin

file_name = sys.argv[1]
url_set = set()

with open(file_name) as file:
    data = file.read()
    pretty_json = json.loads(data)
    nodes = pretty_json["nodes"]
    for node in nodes:
        if("org" in node["secondLevelDomain"]):
            url = urlparse(node["name"])
            url_set.add(url.netloc)

print(url_set)
with open(file_name.replace("_scraped.json", "_unique.txt"), 'w') as f:
    for item in url_set:
        f.write(item)
        f.write("\n")
