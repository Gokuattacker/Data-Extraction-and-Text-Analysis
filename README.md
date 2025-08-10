# Data Extraction and Text Analysis

This project performs text analysis on a collection of articles, extracting various linguistic and sentiment metrics and saving the results to an Excel file.

## Project Structure

- `text_analysis.py` — Main script for analyzing articles and generating output.
- `data_extraction.py` — (Purpose not described here; see file for details.)
- `config.py` — Loads stopwords and master dictionary for sentiment analysis.
- `articles/` — Folder containing `.txt` files to be analyzed.
- `MasterDictionary/` — Contains positive and negative word lists.
- `StopWords/` — Contains stopword lists.
- `Output.xlsx` — Output file with analysis results.
- `requirements.txt` — Python dependencies.

## Requirements

- Python 3.7+
- See `requirements.txt` for required packages (e.g., `nltk`, `openpyxl`).

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Ensure the following folders and files exist:
    - `articles/` with your `.txt` article files.
    - `MasterDictionary/` with positive and negative word lists.
    - `StopWords/` with stopword lists.

3. Download NLTK data (the script will attempt to auto-download if missing).

## Usage

Run the main analysis script:

```sh
python text_analysis.py
```

This will process all `.txt` files in the `articles/` folder and save the results to `Output.xlsx`.

## Output

The output Excel file contains the following columns for each article:

- URL_ID
- POSITIVE SCORE
- NEGATIVE SCORE
- POLARITY SCORE
- SUBJECTIVITY SCORE
- AVG SENTENCE LENGTH
- PERCENTAGE OF COMPLEX WORDS
- FOG INDEX
- AVG NUMBER OF WORDS PER SENTENCE
- COMPLEX WORD COUNT
- WORD COUNT
- SYLLABLE PER WORD
- PERSONAL PRONOUNS
- AVG WORD LENGTH

## Notes

- The script handles Unicode and Latin-1 encoded files.
- Stopwords and sentiment dictionaries are loaded via functions in `config.py`.
