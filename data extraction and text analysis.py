import openpyxl
from bs4 import BeautifulSoup
import requests
import re
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
nltk.download('punkt')
nltk.download('stopwords')

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

    text_dir = "D:\Blackcoffer"
stopwords_dir = "D:\Blackcoffer\StopWords"
sentment_dir = "D:\Blackcoffer\MasterDictionary"

stop_words = set()
for files in os.listdir(stopwords_dir):
  with open(os.path.join(stopwords_dir,files),'r',encoding='ISO-8859-1') as f:
    stop_words.update(set(f.read().splitlines()))

docs = []
for text_file in os.listdir(text_dir):
  with open(os.path.join(text_dir,text_file),'r') as f:
    text = f.read()

    words = word_tokenize(text)

    filtered_text = [word for word in words if word.lower() not in stop_words]

    docs.append(filtered_text)



pos=set()
neg=set()

for files in os.listdir(sentment_dir):
  if files =='positive-words.txt':
    with open(os.path.join(sentment_dir,files),'r',encoding='ISO-8859-1') as f:
      pos.update(f.read().splitlines())
  else:
    with open(os.path.join(sentment_dir,files),'r',encoding='ISO-8859-1') as f:
      neg.update(f.read().splitlines())


positive_words = []
Negative_words =[]
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []

for i in range(len(docs)):
  positive_words.append([word for word in docs[i] if word.lower() in pos])
  Negative_words.append([word for word in docs[i] if word.lower() in neg])
  positive_score.append(len(positive_words[i]))
  negative_score.append(len(Negative_words[i]))
  polarity_score.append((positive_score[i] - negative_score[i]) / ((positive_score[i] + negative_score[i]) + 0.000001))
  subjectivity_score.append((positive_score[i] + negative_score[i]) / ((len(docs[i])) + 0.000001))



avg_sentence_length = []
Percentage_of_Complex_words  =  []
Fog_Index = []
complex_word_count =  []
avg_syllable_word_count =[]

stopwords = set(stopwords.words('english'))
def measure(file):
  with open(os.path.join(text_dir, file),'r') as f:
    text = f.read()

    text = re.sub(r'[^\w\s.]','',text)

    sentences = text.split('.')

    num_sentences = len(sentences)

    words = [word  for word in text.split() if word.lower() not in stopwords ]
    num_words = len(words)

    complex_words = []
    for word in words:
      vowels = 'aeiou'
      syllable_count_word = sum( 1 for letter in word if letter.lower() in vowels)
      if syllable_count_word > 2:
        complex_words.append(word)

    syllable_count = 0
    syllable_words =[]
    for word in words:
      if word.endswith('es'):
        word = word[:-2]
      elif word.endswith('ed'):
        word = word[:-2]
      vowels = 'aeiou'
      syllable_count_word = sum( 1 for letter in word if letter.lower() in vowels)
      if syllable_count_word >= 1:
        syllable_words.append(word)
        syllable_count += syllable_count_word


    avg_sentence_len = num_words / num_sentences
    avg_syllable_word_count = syllable_count / len(syllable_words)
    Percent_Complex_words  =  len(complex_words) / num_words
    Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)

    return avg_sentence_len, Percent_Complex_words, Fog_Index, len(complex_words),avg_syllable_word_count

for file in os.listdir(text_dir):
  x,y,z,a,b = measure(file)
  avg_sentence_length.append(x)
  Percentage_of_Complex_words.append(y)
  Fog_Index.append(z)
  complex_word_count.append(a)
  avg_syllable_word_count.append(b)


def cleaned_words(file):
  with open(os.path.join(text_dir,file), 'r') as f:
    text = f.read()
    text = re.sub(r'[^\w\s]', '' , text)
    words = [word  for word in text.split() if word.lower() not in stopwords]
    length = sum(len(word) for word in words)
    average_word_length = length / len(words)
  return len(words),average_word_length

word_count = []
average_word_length = []
for file in os.listdir(text_dir):
  x, y = cleaned_words(file)
  word_count.append(x)
  average_word_length.append(y)


def count_personal_pronouns(file):
  with open(os.path.join(text_dir,file), 'r') as f:
    text = f.read()
    personal_pronouns = ["I", "we", "my", "ours", "us"]
    count = 0
    for pronoun in personal_pronouns:
      count += len(re.findall(r"\b" + pronoun + r"\b", text)) 
  return count

pp_count = []
for file in os.listdir(text_dir):
  x = count_personal_pronouns(file)
  pp_count.append(x)

output_df = pd.read_excel('Output Data Structure.xlsx')

output_df.drop([44-37,57-37,144-37], axis = 0, inplace=True)

variables = [positive_score,
            negative_score,
            polarity_score,
            subjectivity_score,
            avg_sentence_length,
            Percentage_of_Complex_words,
            Fog_Index,
            avg_sentence_length,
            complex_word_count,
            word_count,
            avg_syllable_word_count,
            pp_count,
            average_word_length]

for i, var in enumerate(variables):
  output_df.iloc[:,i+2] = var

output_df.to_csv('Output_Data.csv')
