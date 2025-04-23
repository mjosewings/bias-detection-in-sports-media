#This file is responsible for the Flask server that handles the API requests and responses
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io
import base64
import sys
from pathlib import Path
from transcript import get_video_comments, save_comments

# Add NBA and WNBA directories to Python path for importing
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root / 'NBA'))
sys.path.append(str(project_root / 'WNBA'))

app = Flask(__name__)
CORS(app)

# Sets up logging
@app.route('/api/analyze', methods=['POST'])
# Function responsible for analyzing the video comments
def analyze_video():
    data = request.get_json()
    league = data.get('league')

    # New fields for both mode
    video_id_nba = data.get('videoId_nba')
    video_id_wnba = data.get('videoId_wnba')
    video_id = data.get('videoId')

    # Check if video_id is provided for single league
    try:
        if league == 'nba':
            comments = get_video_comments(video_id)
            if not comments:
                return jsonify({'error': 'No NBA comments retrieved'}), 500

            # Save comments to a file
            comment_file = save_comments(video_id, comments)
            nba_cleaned = f'{video_id}_nba_processed_comments.csv'
            nba_excel = f'{video_id}_nba_analysis_sentiment_results.xlsx'

            # Run the cleaning and analysis scripts
            subprocess.run(['python', 'NBA/Comments_NBA/nba_data_cleaning.py', comment_file], check=True)
            subprocess.run(['python', 'NBA/Comments_NBA/nba_bias_analysis.py', nba_cleaned], check=True)

            results = generate_visualizations(nba_excel, 'NBA')
            clean_generated_files([video_id, video_id_nba, video_id_wnba]) # File Cleanup
            return jsonify(results)

        elif league == 'wnba':
            comments = get_video_comments(video_id)
            if not comments:
                return jsonify({'error': 'No WNBA comments retrieved'}), 500

            # Save comments to a file
            comment_file = save_comments(video_id, comments)
            wnba_cleaned = f'{video_id}_wnba_processed_comments.csv'
            wnba_excel = f'{video_id}_wnba_analysis_sentiment_results.xlsx'

            # Run the cleaning and analysis scripts
            subprocess.run(['python', 'WNBA/Comments_WNBA/wnba_data_cleaning.py', comment_file], check=True)
            subprocess.run(['python', 'WNBA/Comments_WNBA/wnba_bias_analysis.py', wnba_cleaned], check=True)

            results = generate_visualizations(wnba_excel, 'WNBA')
            clean_generated_files([video_id, video_id_nba, video_id_wnba]) # File Cleanup
            return jsonify(results)

        elif league == 'both':
            video_id_nba = data.get('videoId_nba')
            video_id_wnba = data.get('videoId_wnba')

            print("[DEBUG] video_id_nba:", video_id_nba)
            print("[DEBUG] video_id_wnba:", video_id_wnba)

            comments_nba = get_video_comments(video_id_nba)
            comments_wnba = get_video_comments(video_id_wnba)

            if not comments_nba:
                return jsonify({'error': 'No NBA comments retrieved'}), 500
            if not comments_wnba:
                return jsonify({'error': 'No WNBA comments retrieved'}), 500

            file_nba = save_comments(video_id_nba, comments_nba)
            file_wnba = save_comments(video_id_wnba, comments_wnba)

            cleaned_nba = f'{video_id_nba}_nba_processed_comments.csv'
            excel_nba = f'{video_id_nba}_nba_analysis_sentiment_results.xlsx'
            cleaned_wnba = f'{video_id_wnba}_wnba_processed_comments.csv'
            excel_wnba = f'{video_id_wnba}_wnba_analysis_sentiment_results.xlsx'

            # Run the cleaning and analysis scripts
            subprocess.run(['python', 'NBA/Comments_NBA/nba_data_cleaning.py', file_nba], check=True)
            subprocess.run(['python', 'NBA/Comments_NBA/nba_bias_analysis.py', cleaned_nba], check=True)
            subprocess.run(['python', 'WNBA/Comments_WNBA/wnba_data_cleaning.py', file_wnba], check=True)
            subprocess.run(['python', 'WNBA/Comments_WNBA/wnba_bias_analysis.py', cleaned_wnba], check=True)

            results = []
            results += generate_visualizations(excel_nba, 'NBA')
            results += generate_visualizations(excel_wnba, 'WNBA')

            results.append(generate_bias_comparison_chart(excel_nba, excel_wnba))
            clean_generated_files([video_id, video_id_nba, video_id_wnba]) # File Cleanup
            return jsonify(results)
            

        else:
            return jsonify({'error': 'Invalid league selected'}), 400

    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Subprocess failed: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


# Function to generate visualizations (Charts and Graphs)
def generate_visualizations(filepath, title_prefix):
    df_dict = pd.read_excel(filepath, sheet_name=None)
    sentiment_df = df_dict['Sentiment Analysis']
    bias_df = df_dict['Bias Analysis']
    results = []

    # Pie Chart
    sentiments = {
        'Positive': (sentiment_df['sentiment_score'] > 0).sum(),
        'Neutral': (sentiment_df['sentiment_score'] == 0).sum(),
        'Negative': (sentiment_df['sentiment_score'] < 0).sum()
    }
    fig1, ax1 = plt.subplots()
    ax1.pie(sentiments.values(), labels=sentiments.keys(), autopct='%1.1f%%', startangle=140)
    ax1.set_title(f'{title_prefix} Sentiment Distribution')
    results.append({
        'title': f'{title_prefix} Sentiment Pie',
        'type': 'pie',
        'image': fig_to_base64(fig1)
    })

    # Box Plot
    sentiment_df['sentiment_category'] = sentiment_df['sentiment_score'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=sentiment_df, x='sentiment_category', y='sentiment_score', ax=ax2)
    ax2.set_title(f'{title_prefix} Sentiment Box Plot')
    results.append({
        'title': f'{title_prefix} Sentiment Box',
        'type': 'boxplot',
        'image': fig_to_base64(fig2)
    })

    # Word Cloud
    text = ' '.join(sentiment_df['content'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig3, ax3 = plt.subplots()
    ax3.imshow(wordcloud, interpolation='bilinear')
    ax3.axis('off')
    ax3.set_title(f'{title_prefix} Word Cloud')
    results.append({
        'title': f'{title_prefix} Word Cloud',
        'type': 'wordcloud',
        'image': fig_to_base64(fig3)
    })

    # Bar Chart for Bias
    fig4, ax4 = plt.subplots()
    bias_df.plot.barh(x='Bias Category', y='Bias Count', ax=ax4, color='green', alpha=0.7)
    ax4.set_title(f'{title_prefix} Bias Chart')
    results.append({
        'title': f'{title_prefix} Bias Bar Chart',
        'type': 'barchart',
        'image': fig_to_base64(fig4)
    })

    return results

# Function to generate bias comparison chart between NBA and WNBA
def generate_bias_comparison_chart(excel_nba_path, excel_wnba_path):
    # Load the Bias Analysis sheets
    nba_df = pd.read_excel(excel_nba_path, sheet_name='Bias Analysis')
    wnba_df = pd.read_excel(excel_wnba_path, sheet_name='Bias Analysis')

    # Merge on Bias Category
    merged_df = pd.merge(nba_df, wnba_df, on='Bias Category', suffixes=('_NBA', '_WNBA'))

    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(merged_df['Bias Category'], merged_df['Bias Count_NBA'], color='blue', alpha=0.6, label='NBA')
    ax.barh(merged_df['Bias Category'], merged_df['Bias Count_WNBA'], color='green', alpha=0.6, label='WNBA')
    ax.set_xlabel('Bias Count')
    ax.set_title('Bias Comparison Between NBA and WNBA')
    ax.legend()

    # Convert to base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {
        'title': 'NBA vs WNBA Bias Comparison',
        'type': 'comparison_barchart',
        'image': img_base64
    }

# Function to clean up generated files after analysis
def clean_generated_files(video_ids):
    suffixes = [
        '_comments.txt',
        '_nba_processed_comments.csv',
        '_wnba_processed_comments.csv',
        '_nba_analysis_sentiment_results.xlsx',
        '_wnba_analysis_sentiment_results.xlsx',
        '_nba_word_frequencies.csv',
        '_wnba_word_frequencies.csv',
        '_nba_unique_words.csv',
        '_wnba_unique_words.csv',
        '_bias_bar_chart.png'
    ]

    for vid in video_ids:
        for suffix in suffixes:
            file_path = f'{vid}{suffix}'
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'[CLEANUP] Removed: {file_path}')

# Function to convert matplotlib figure to base64 string
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
