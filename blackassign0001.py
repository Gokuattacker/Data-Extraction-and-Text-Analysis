import requests
from bs4 import BeautifulSoup

url = "https://insights.blackcoffer.com/rise-of-internet-demand-and-its-impact-on-communications-and-alternatives-by-the-year-2035-2/"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

title = soup.title.text
paragraphs = soup.find_all('p')

title_tag = soup.find('title')




filename = "blackassign0010.txt"

with open(filename, 'w', encoding='utf-8') as file:
    file.write("Title: " + title + "\n\n")
    file.write("Paragraphs:\n")
    for paragraph in paragraphs:
        file.write(paragraph.text + "\n")


