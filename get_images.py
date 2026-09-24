import urllib.request
import re

url = "https://www.printables.com/model/981111-dummy-13-version-10"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    urls = re.findall(r'https://media\.printables\.com/media/prints/[^\"\'\s]+\.webp', html)
    print("\n".join(set(urls)))
except Exception as e:
    print(e)
