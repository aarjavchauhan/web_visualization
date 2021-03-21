
from urllib.parse import urlparse, urljoin
import tldextract

test_url = "https://war.wikipedia.org/wiki/Internet"


domain = tldextract.extract(test_url)

print(domain)

