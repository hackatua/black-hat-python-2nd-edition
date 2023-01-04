import urllib.parse
import urllib.request

url = 'https://jsonplaceholder.typicode.com/posts'
data = {
    "name": "test",
    "salary": "123",
    "age": "23"
}

encoded_data = urllib.parse.urlencode(data).encode()
req = urllib.request.Request(url, encoded_data)
with urllib.request.urlopen(req) as response:
    content = response.read()
    print(content)