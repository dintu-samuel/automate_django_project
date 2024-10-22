from bs4 import BeautifulSoup
import requests

url ='https://webscraper.io/test-sites/tables'
response = requests.get(url)

# print(response.content)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)

heading1 = soup.find_all('h2').text
print(heading1)