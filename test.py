import pandas as pd
import requests
from bs4 import BeautifulSoup

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

    df['Title'] = ''
    df['Article Text'] = ''

    for index, row in df.iterrows():
        url = row['B']

        title, article_text = extract_article(url)

        df.at[index, 'Title'] = title
        df.at[index, 'Article Text'] = article_text

    output_file = f"{output_folder}/output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Extracted data saved to {output_file}")

if __name__ == "__main__":
    input_file_path = 'C:\Users\abhig\Downloads\Input.xlsx'

    output_folder_path = 'D:\college'

    import os
    os.makedirs(output_folder_path, exist_ok=True)

    process_excel(input_file_path, output_folder_path)
