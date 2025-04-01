import nltk
import string
import re
import csv
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Text Preprocessing Function
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove numbers and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens

# Load and preprocess text from a file
def preprocess_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return preprocess_text(text)

# Save unique words to CSV
def save_unique_words_to_csv(tokens, output_file):
    unique_words = list(set(tokens))  # Remove duplicates
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Unique_Words"])
        for word in unique_words:
            writer.writerow([word])

# Save word frequencies to CSV
def save_word_frequencies_to_csv(tokens, output_file):
    word_counts = Counter(tokens)  # Count occurrences of each word
    df = pd.DataFrame(word_counts.items(), columns=["Word", "Frequency"])
    df = df.sort_values(by="Frequency", ascending=False)  # Sort by most frequent words
    df.to_csv(output_file, index=False)

# Main logic
file_path = 'The_Day_Caitlin_Clark_Showed_Angel_Reese_Who’s_Boss_comments.txt'  # Update with your file path
unique_words_csv = 'wnba_unique_words.csv'  # Output CSV file for unique words
word_frequencies_csv = 'wnba_word_frequencies.csv'  # Output CSV file for word counts

processed_text = preprocess_from_file(file_path)

# Save results
save_unique_words_to_csv(processed_text, unique_words_csv)
save_word_frequencies_to_csv(processed_text, word_frequencies_csv)

print(f"NBA Unique words saved to {unique_words_csv}")
print(f"NBA Word frequencies saved to {word_frequencies_csv}")
