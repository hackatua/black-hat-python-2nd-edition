import urllib.parse
import urllib.request

url = 'http://google.com'
with urllib.request.urlopen(url) as response:
    content = response.read()
    print(content)