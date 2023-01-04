import requests

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

print(response.text)