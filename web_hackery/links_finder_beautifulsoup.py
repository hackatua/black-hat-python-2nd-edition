from bs4 import BeautifulSoup as bs
import requests

url = "https://nostarch.com"
response = requests.get(url)

tree = bs(response.text, 'html.parser')

for link in tree.find_all('a'):
    print(f"{link.get('href')} -> {link.text}")