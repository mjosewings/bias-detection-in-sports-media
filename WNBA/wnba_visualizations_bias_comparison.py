import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# Define paths to the NBA and WNBA files
nba_file_path = './NBA/nba_analysis_sentiment_results.xlsx'  # Update if necessary
wnba_file_path = './WNBA/wnba_analysis_sentiment_results.xlsx'  # Update if necessary

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
nba_df = pd.read_excel(nba_file_path, sheet_name=None)  # Assuming two sheets: 'Bias Analysis', 'Sentiment Analysis'
wnba_df = pd.read_excel(wnba_file_path, sheet_name=None)

# Extract individual sheets as DataFrames (if needed)
nba_bias_df = nba_df['Bias Analysis']
nba_sentiment_df = nba_df['Sentiment Analysis']
wnba_bias_df = wnba_df['Bias Analysis']
wnba_sentiment_df = wnba_df['Sentiment Analysis']

# Function to plot pie chart
def plot_sentiment_pie_chart(df, title):
    sentiment_counts = df['Sentiment'].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
            colors=['#66b3ff', '#ff9999', '#66ff66'])
    plt.title(f'Sentiment Distribution: {title}')
    plt.show()

    # Save plot
    plt.savefig(f'{title}_sentiment_pie_chart.png', bbox_inches='tight')  # Save pie chart to file
    print(f"Saved {title}_sentiment_pie_chart.png")

# Plot pie charts for both NBA and WNBA sentiment analysis
plot_sentiment_pie_chart(nba_sentiment_df, "NBA")
plot_sentiment_pie_chart(wnba_sentiment_df, "WNBA")

# Function to plot box plot
def plot_sentiment_box_plot(df, title):
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='Sentiment', y='Sentiment Score', palette='Set2')
    plt.title(f'Sentiment Scores Distribution: {title}')
    plt.show()

    # Save plot
    plt.savefig(f'{title}_sentiment_box_plot.png', bbox_inches='tight')  # Save box plot to file
    print(f"Saved {title}_sentiment_box_plot.png")

# Plot box plots for both NBA and WNBA sentiment analysis
plot_sentiment_box_plot(nba_sentiment_df, "NBA")
plot_sentiment_box_plot(wnba_sentiment_df, "WNBA")

# Function to generate word cloud
def generate_word_cloud(df, title):
    text = " ".join(df['Content'].dropna().tolist())  # Join all comments into one large string
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud: {title}')
    plt.axis('off')
    plt.show()

    # Save plot
    plt.savefig(f'{title}_word_cloud.png', bbox_inches='tight')  # Save word cloud to file
    print(f"Saved {title}_word_cloud.png")

# Generate word clouds for both NBA and WNBA media coverage
generate_word_cloud(nba_sentiment_df, "NBA")
generate_word_cloud(wnba_sentiment_df, "WNBA")

# Function to plot bar chart
def plot_bias_bar_chart(nba_bias_df, wnba_bias_df, title):
    plt.figure(figsize=(12, 8))
    plt.barh(nba_bias_df['Bias Category'], nba_bias_df['Bias Count'], color='blue', alpha=0.6, label='NBA')
    plt.barh(wnba_bias_df['Bias Category'], wnba_bias_df['Bias Count'], color='green', alpha=0.6, label='WNBA')

    plt.xlabel('Bias Count')
    plt.ylabel('Bias Category')
    plt.title(f'Bias Count Comparison: {title}')
    plt.legend()
    plt.show()

    # Save plot
    plt.savefig(f'{title}_bias_bar_chart.png', bbox_inches='tight')  # Save bar chart to file
    print(f"Saved {title}_bias_bar_chart.png")

# Plot bar chart comparing bias counts for NBA and WNBA
plot_bias_bar_chart(nba_bias_df, wnba_bias_df, "NBA vs. WNBA Bias Comparison")

# Optionally, save all plots into a directory
output_dir = './visualizations'
os.makedirs(output_dir, exist_ok=True)

# Example for saving the pie chart
fig = plt.figure(figsize=(7, 7))
save_plot_as_file(fig, os.path.join(output_dir, 'sentiment_pie_chart.png'))
