# wnba_data_cleaning.py
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

if len(sys.argv) < 2:
    print("Usage: python wnba_data_cleaning.py <comments_txt_file>")
    exit(1)

input_file = sys.argv[1]
base_name = input_file.replace('_comments.txt', '')

# Step 1: Load raw comments
with open(input_file, 'r', encoding='utf-8') as f:
    raw_comments = f.readlines()

# Step 2: Clean comments
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
cleaned_comments = []

for comment in raw_comments:
    comment = comment.lower()
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(comment)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]
    cleaned_comments.append(' '.join(tokens))

# Step 3: Save processed data
df = pd.DataFrame({
    'content': raw_comments,
    'cleaned': cleaned_comments
})
cleaned_csv = f'{base_name}_wnba_processed_comments.csv'
df.to_csv(cleaned_csv, index=False)

# Step 4: Generate word frequencies
all_words = ' '.join(cleaned_comments).split()
word_freq = Counter(all_words)

word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
word_freq_df.sort_values(by='Frequency', ascending=False, inplace=True)
word_freq_df.to_csv(f'{base_name}_wnba_word_frequencies.csv', index=False)

unique_words_df = pd.DataFrame({'Word': list(set(all_words))})
unique_words_df.to_csv(f'{base_name}_wnba_unique_words.csv', index=False)

print(f"[INFO] Cleaning complete. Saved to {cleaned_csv}")
