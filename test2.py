import openpyxl
from bs4 import BeautifulSoup
import requests
import re

def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').get_text(strip=True) if soup.find('title') else "No Title"

        article_text = ''
        article_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section'])
        for tag in article_tags:
            article_text += tag.get_text(strip=True) + '\n'

        return title, article_text

    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None, None

def save_to_text_file(url_id, title, article_text):
    filename = f"{url_id}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n\n{article_text}")

if __name__ == "__main__":
    
    excel_file = 'Input.xlsx'
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        url_id, url = row
        title, article_text = extract_article_text(url)

        if title is not None and article_text is not None:
            save_to_text_file(url_id, title, article_text)

    print("Extraction and saving completed.")
