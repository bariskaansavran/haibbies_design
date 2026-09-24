import urllib.request
import re
import urllib.parse

url = "https://html.duckduckgo.com/html/?q=nespresso+pod+holder+under+cabinet+jpg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'//external-content\.duckduckgo\.com/iu/\?u=([^&]+)', html)
    for img in list(set(images))[:5]:
        print(urllib.parse.unquote(img))
except Exception as e:
    print("Error:", e)
