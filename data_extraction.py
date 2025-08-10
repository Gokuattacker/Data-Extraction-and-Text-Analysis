import openpyxl
import requests
from bs4 import BeautifulSoup
import os
import re

INPUT_FILE = "Input.xlsx"
OUTPUT_FOLDER = "articles"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Adjust selectors depending on site structure
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return f"{title}\n{text}"
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def main():
    wb = openpyxl.load_workbook(INPUT_FILE)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        url_id, url = row
        article_text = extract_article(url)
        if article_text:
            with open(os.path.join(OUTPUT_FOLDER, f"{url_id}.txt"), "w", encoding="utf-8") as f:
                f.write(article_text)
            print(f"Saved {url_id}.txt")

if __name__ == "__main__":
    main()
