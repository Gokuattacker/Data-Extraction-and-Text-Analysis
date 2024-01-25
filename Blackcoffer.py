import requests
from bs4 import BeautifulSoup

url = "https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

title = soup.title.text
paragraphs = soup.find_all('p')

filename = "blackassign0018.txt"

with open(filename, 'w', encoding='utf-8') as file:
    file.write("Title: " + title + "\n\n")
    file.write("Paragraphs:\n")
    for paragraph in paragraphs:
        file.write(paragraph.text + "\n")


