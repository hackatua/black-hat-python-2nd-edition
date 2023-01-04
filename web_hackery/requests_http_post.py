import requests

url = "https://jsonplaceholder.typicode.com/guide/"
data = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

response = requests.post(url, data=data)

print(response.text)