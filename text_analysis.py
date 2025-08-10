import os
import re
import openpyxl
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from config import load_stopwords, load_master_dictionary

# --- Auto-download NLTK resources ---
for resource in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        if resource in ['punkt', 'punkt_tab']:
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
    except LookupError:
        nltk.download(resource)

ARTICLES_FOLDER = "articles"
OUTPUT_FILE = "Output.xlsx"

# Load stopwords and dictionaries
stop_words = load_stopwords()
positive_words, negative_words = load_master_dictionary()

def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word and word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith(("es", "ed")):
        count -= 1
    return max(1, count)

def analyze_text(text):
    tokens = word_tokenize(text.lower())
    words_all = [w for w in tokens if w.isalpha()]  # Keep all alpha words
    words = [w for w in words_all if w not in stop_words]  # For sentiment & other metrics

    sentences = sent_tokenize(text)

    pos_score = sum(1 for w in words if w in positive_words)
    neg_score = sum(1 for w in words if w in negative_words)

    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)
    subjectivity = (pos_score + neg_score) / (len(words) + 0.000001)

    avg_sent_len = len(words) / len(sentences) if sentences else 0
    complex_words = [w for w in words if count_syllables(w) > 2]
    pct_complex = len(complex_words) / len(words) if words else 0
    fog_index = 0.4 * (avg_sent_len + pct_complex)

    avg_words_per_sent = len(words) / len(sentences) if sentences else 0
    complex_word_count = len(complex_words)
    word_count = len(words)
    syllable_per_word = sum(count_syllables(w) for w in words) / len(words) if words else 0

    pronouns = len(re.findall(r"\b(I|we|my|ours|us)\b", text, re.I))
    avg_word_len = sum(len(w) for w in words_all) / len(words_all) if words_all else 0


    return [
        pos_score, neg_score, polarity, subjectivity, avg_sent_len,
        pct_complex, fog_index, avg_words_per_sent, complex_word_count,
        word_count, syllable_per_word, pronouns, avg_word_len
    ]

def main():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append([
        "URL_ID", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE",
        "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
        "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT",
        "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ])

    for file in os.listdir(ARTICLES_FOLDER):
        if file.endswith(".txt"):
            url_id = os.path.splitext(file)[0]

            # --- Encoding fallback when reading articles ---
            file_path = os.path.join(ARTICLES_FOLDER, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    text = f.read()

            metrics = analyze_text(text)
            sheet.append([url_id] + metrics)

    wb.save(OUTPUT_FILE)
    print(f"Saved analysis to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
