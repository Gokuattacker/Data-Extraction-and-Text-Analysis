import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def extract_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.text.strip()

        article_content = soup.find('div', class_='article-content')  

        article_text = ""
        if article_content:
            for paragraph in article_content.find_all('p'):
                article_text += paragraph.text + "\n"

        return title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None, None

def process_excel(input_file, output_folder):
    
    df = pd.read_excel(input_file, sheet_name='input')

    os.makedirs(output_folder, exist_ok=True)

    for index, row in df.iterrows():
        url = row['B']

        title, article_text = extract_article(url)

        output_file_path = os.path.join(output_folder, f"{index + 1}_{title}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Title: {title}\n\n")
            output_file.write("Article Text:\n")
            output_file.write(article_text)

    print(f"Extracted data saved to {output_folder}")

if __name__ == "__main__":
    input_file_path = 'D:\Blackcoffer\Input.xlsx'

    output_folder_path = 'D:\Blackcoffer'

    process_excel(input_file_path, output_folder_path)
