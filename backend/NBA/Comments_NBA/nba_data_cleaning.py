# This file is responsible for cleaning and processing NBA comments from a text file
import sys
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Check to see if the input file is provided
if len(sys.argv) < 2:
    print("Usage: python nba_data_cleaning.py <comments_txt_file>")
    exit(1)

input_file = sys.argv[1]
base_name = input_file.replace('_comments.txt', '')

#Loads raw Comments
with open(input_file, 'r', encoding='utf-8') as f:
    raw_comments = f.readlines()

#Cleans comments by getting rid of punctuation, stop words, and lemmatizing
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
cleaned_comments = []

for comment in raw_comments:
    comment = comment.lower()
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(comment)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]
    cleaned_comments.append(' '.join(tokens))

#Saves the cleaned comments to a new CSV file
df = pd.DataFrame({
    'content': raw_comments,
    'cleaned': cleaned_comments
})
cleaned_csv = f'{base_name}_nba_processed_comments.csv'
df.to_csv(cleaned_csv, index=False)

#Generates word frequency and unique words and puts into CSV files
all_words = ' '.join(cleaned_comments).split()
word_freq = Counter(all_words)

word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
word_freq_df.sort_values(by='Frequency', ascending=False, inplace=True)
word_freq_df.to_csv(f'{base_name}_nba_word_frequencies.csv', index=False)

unique_words_df = pd.DataFrame({'Word': list(set(all_words))})
unique_words_df.to_csv(f'{base_name}_nba_unique_words.csv', index=False)

print(f"[INFO] Cleaning complete. Saved to {cleaned_csv}")
