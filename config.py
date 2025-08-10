import os

# Paths
STOPWORDS_FOLDER = "StopWords"
MASTER_DICT_FOLDER = "MasterDictionary"
OUTPUT_STRUCTURE_FILE = "Output Data Structure.xlsx"

# Load stopwords
def load_stopwords():
    stop_words = set()
    for file in os.listdir(STOPWORDS_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(STOPWORDS_FOLDER, file), "r", encoding="utf-8") as f:
                stop_words.update([line.strip().lower() for line in f if line.strip()])
    return stop_words

# Load positive & negative words
def load_master_dictionary():
    positive_words = set()
    negative_words = set()
    for file in os.listdir(MASTER_DICT_FOLDER):
        filepath = os.path.join(MASTER_DICT_FOLDER, file)
        with open(filepath, "r", encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
            if "positive" in file.lower():
                positive_words.update(words)
            elif "negative" in file.lower():
                negative_words.update(words)
    return positive_words, negative_words
