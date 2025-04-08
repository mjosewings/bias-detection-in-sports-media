import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
from pathlib import Path

# Get the current script location
project_root = Path(__file__).parent.parent.parent

# Construct paths based on the project root
nba_file_path = project_root / 'NBA' / 'Bias Analysis Model - NBA' / 'nba_analysis_sentiment_results.xlsx'
wnba_file_path = project_root / 'WNBA' / 'Bias Analysis Model - WNBA' / 'wnba_analysis_sentiment_results.xlsx'

# Check if files exist
if not os.path.exists(nba_file_path):
    print(f"NBA file not found at {nba_file_path}")
else:
    print(f"NBA file found at {nba_file_path}")

if not os.path.exists(wnba_file_path):
    print(f"WNBA file not found at {wnba_file_path}")
else:
    print(f"WNBA file found at {wnba_file_path}")

# Load the NBA and WNBA datasets
nba_df = pd.read_excel(nba_file_path, sheet_name=None)
nba_sentiment_full_df = nba_df['Full Sentiment Data']  # Assuming two sheets: 'Bias Analysis', 'Sentiment Analysis'
wnba_df = pd.read_excel(wnba_file_path, sheet_name=None)
wnba_sentiment_full_df = wnba_df['Full Sentiment Data']

# Extract individual sheets as DataFrames (if needed)
nba_bias_df = nba_df['Bias Analysis']
#nba_sentiment_full_df = nba_df['Sentiment Analysis']
wnba_bias_df = wnba_df['Bias Analysis']
#wnba_sentiment_full_df = wnba_df['Sentiment Analysis']
print(nba_sentiment_full_df.columns)
# Function to plot pie chart
def plot_sentiment_pie_chart(df, title):

    # Categorize sentiment
    grouped_sentiments = {
        'Positive': (df['sentiment_score'] > 0).sum(),
        'Neutral': (df['sentiment_score'] == 0).sum(),
        'Negative': (df['sentiment_score'] < 0).sum()
    }

    labels = list(grouped_sentiments.keys())
    sizes = list(grouped_sentiments.values())
    colors = ['#66ff66', '#66b3ff', '#ff9999']  # Positive, Neutral, Negative

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title(f'Sentiment Distribution: {title}')

    # Save plot first, then show it
    plt.savefig(f'{title}_sentiment_pie_chart.png', bbox_inches='tight')
    plt.show()
    print(f"Saved {title}_sentiment_pie_chart.png")

# Plot pie charts for both NBA and WNBA sentiment analysis
plot_sentiment_pie_chart(nba_sentiment_full_df, "NBA")
plot_sentiment_pie_chart(wnba_sentiment_full_df, "WNBA")

def plot_sentiment_box_plot(df, title):
    if 'sentiment_category' not in df.columns:
        df['sentiment_category'] = df['sentiment_score'].apply(
            lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='sentiment_category', y='sentiment_score')
    sns.stripplot(data=df, x='sentiment_category', y='sentiment_score',
                  order=['Negative', 'Neutral', 'Positive'],
                  color='black', alpha=0.3, jitter=True)
    plt.title(f'Sentiment Scores Distribution: {title}')

    plt.savefig(f'{title}_sentiment_box_plot.png', bbox_inches='tight')
    plt.show()
    print(f"Saved {title}_sentiment_box_plot.png")

# Plot box plots for both NBA and WNBA sentiment analysis
plot_sentiment_box_plot(nba_sentiment_full_df, "NBA")
plot_sentiment_box_plot(wnba_sentiment_full_df, "WNBA")

# Function to generate word cloud
def generate_word_cloud(df, title):
    text = " ".join(df['content'].dropna().tolist())  # Join all comments into one large string
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud: {title}')
    plt.axis('off')


    # Save plot
    plt.savefig(f'{title}_word_cloud.png', bbox_inches='tight')  # Save word cloud to file
    plt.show()
    print(f"Saved {title}_word_cloud.png")

# Generate word clouds for both NBA and WNBA media coverage
generate_word_cloud(nba_sentiment_full_df, "NBA")
generate_word_cloud(wnba_sentiment_full_df, "WNBA")

# Function to plot bar chart
def plot_bias_bar_chart(nba_bias_df, wnba_bias_df, title):
    plt.figure(figsize=(12, 8))
    plt.barh(nba_bias_df['Bias Category'], nba_bias_df['Bias Count'], color='blue', alpha=0.6, label='NBA')
    plt.barh(wnba_bias_df['Bias Category'], wnba_bias_df['Bias Count'], color='green', alpha=0.6, label='WNBA')

    plt.xlabel('Bias Count')
    plt.ylabel('Bias Category')
    plt.title(f'Bias Count Comparison: {title}')
    plt.legend()


    # Save plot
    plt.savefig(f'{title}_bias_bar_chart.png', bbox_inches='tight')  # Save bar chart to file
    plt.show()
    print(f"Saved {title}_bias_bar_chart.png")

# Plot bar chart comparing bias counts for NBA and WNBA
plot_bias_bar_chart(nba_bias_df, wnba_bias_df, "NBA vs. WNBA Bias Comparison")

# Optionally, save all plots into a directory
output_dir = './visualizations'
os.makedirs(output_dir, exist_ok=True)

