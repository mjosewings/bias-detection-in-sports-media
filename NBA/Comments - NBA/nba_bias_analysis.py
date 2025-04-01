import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

# Expanded Bias Lexicon
bias_lexicon = {
    "physicality_bias": ["strong", "aggressive", "dominant", "athletic", "big",
                         "tall", "heavy", "muscular", "powerful", "nimble",
                         "weak", "fragile", "clumsy", "graceful", "sturdy",
                         "quick", "slow", "explosive", "energetic", "brute",
                         "bulky", "beast", "massive", "scrawny", "frail",
                         "sluggish", "bouncy", "springy"],

    "emotional_bias": ["emotional", "passionate", "whiny", "sensitive", "soft",
                       "volatile", "irrational", "unstable", "overreacting",
                       "temperamental", "hot-headed", "crybaby", "moody",
                       "dramatic", "fiery", "petulant", "excitable", "calm",
                       "level-headed", "stoic", "composed"],

    "diminishing_bias": ["lucky", "overachiever", "underdog", "hidden gem",
                         "not expected to succeed", "surprisingly good", "fluke",
                         "carried", "system player", "role player", "flash in the pan",
                         "one-hit wonder", "product of the system", "passenger",
                         "filler", "barely made it", "non-factor"],

    "success_bias": ["earned it", "proven", "elite", "grinder", "hard worker",
                     "self-made", "determined", "tenacious", "deserved",
                     "natural talent", "born winner", "championship DNA",
                     "winner", "clutch", "cold-blooded", "fearless",
                     "killer instinct", "mentally tough", "built different",
                     "dog in him", "alpha"],

    "class_bias": ["classless", "ghetto", "thug", "spoiled", "arrogant", "disrespectful",
                   "humble", "trash talk", "punk", "brat", "ungrateful",
                   "reckless", "low-class", "entitled", "cocky",
                   "chip on his shoulder", "villain", "disgraceful",
                   "selfish", "show-off", "egotistical"],

    "racial_bias": ["black", "white", "racist", "privilege", "thug", "lazy",
                    "angry", "hostile", "entitled", "hyperactive",
                    "athletic", "natural ability", "streetball", "fundamentals",
                    "smart player", "high IQ", "crafty", "deceptive quickness",
                    "gritty", "hard-nosed", "blue-collar", "coach’s son"],

    "skill_bias": ["talented", "skilled", "outplayed", "elite", "average", "mediocre",
                   "flawless", "superior", "underperforming",
                   "raw", "unpolished", "mechanical", "fundamental",
                   "basketball IQ", "cerebral", "gifted", "technician",
                   "smooth", "one-dimensional", "versatile",
                   "jack of all trades", "limited", "unstoppable"],

    "appearance_bias": ["handsome", "ugly", "scruffy", "muscular", "heavyset", "plain",
                        "disheveled", "unattractive", "lean", "chiseled",
                        "fit", "bulky", "skinny", "shredded", "big-bodied",
                        "lanky", "well-groomed", "tatted", "clean-cut",
                        "baby-faced", "aging poorly", "dad bod"],

    "gender/sexuality_bias": ["man", "masculine", "dominant", "effeminate", "unmanly",
                              "tomboy", "queer", "gay", "bisexual",
                              "soft", "dainty", "delicate", "sassy",
                              "flamboyant", "metrosexual", "alpha male",
                              "feminine", "intimidating", "powerful"],

    "age_bias": ["young", "old", "veteran", "rookie", "past his prime",
                 "over the hill", "aging", "too young", "washed up",
                 "seasoned", "savvy", "experienced", "grizzled",
                 "battle-tested", "mature", "still got it", "aging gracefully",
                 "declining", "burned out", "mentor role"],

    "disability_bias": ["injury-prone", "fragile", "weak", "impaired", "disabled", "crippled",
                        "damaged goods", "glass bones", "soft tissue issues",
                        "stiff", "hobbled", "limited mobility",
                        "not the same after injury", "past his best", "injury history"],

    "team_affiliation_bias": ["bandwagon", "loyal fan", "diehard", "fairweather",
                              "underdog team", "glory hunter", "casual fan",
                              "jumped ship", "fake fan", "true supporter",
                              "hometown hero", "only roots for winners",
                              "homegrown talent", "mercenary", "superteam",
                              "dynasty chaser", "ring chaser"]
}


# Function: Detect Bias
def detect_bias(word_freq_df):
    word_counts = word_freq_df.set_index('word')['frequency'].to_dict()
    bias_counts = {bias_category: 0 for bias_category in bias_lexicon}

    for bias_category, keywords in bias_lexicon.items():
        bias_counts[bias_category] = sum(word_counts.get(word, 0) for word in keywords)

    return bias_counts


# Function: Perform Sentiment Analysis
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    return sentiment_score['compound']


# Function: Sentiment by Bias
def analyze_sentiment_by_bias(df, bias_lexicon):
    sentiment_by_bias = {bias_category: {'positive': 0, 'negative': 0, 'neutral': 0} for bias_category in bias_lexicon}

    for _, row in df.iterrows():
        comment = row['content']
        sentiment = row['sentiment_category']

        for bias_category, keywords in bias_lexicon.items():
            if any(keyword in comment.lower() for keyword in keywords):
                sentiment_by_bias[bias_category][sentiment.lower()] += 1

    return sentiment_by_bias


# Load the dataset
input_file = 'LeBron_&_AD_Too_Big_For_Curry_|_Game_1_Lakers_v_Warriors_2023_NBA_Playoffs_comments.txt'
output_file = '../Bias Analysis Model - NBA/nba_analysis_sentiment_results.xlsx'

# Read input file as plain text
try:
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Convert to DataFrame (each line is a comment)
    df = pd.DataFrame({"content": [line.strip() for line in lines if line.strip()]})  # Remove empty lines

except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Apply sentiment analysis
df['sentiment_score'] = df['content'].apply(analyze_sentiment)

# Categorize sentiment into Positive, Neutral, or Negative
df['sentiment_category'] = df['sentiment_score'].apply(
    lambda x: 'Positive' if x > 0.05 else 'Negative' if x < -0.05 else 'Neutral')

# Sentiment Analysis Summary
sentiment_summary = df['sentiment_category'].value_counts().reset_index()
sentiment_summary.columns = ['Sentiment', 'Count']

# Tokenize and compute word frequency
vectorizer = CountVectorizer(stop_words='english')
word_freq_matrix = vectorizer.fit_transform(df['content'])

# Convert matrix to a DataFrame with words as columns
word_freq_df = pd.DataFrame(word_freq_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Reshape word frequency data to match bias detection function
word_freq_df = word_freq_df.sum().reset_index()
word_freq_df.columns = ['word', 'frequency']

# Perform bias detection
bias_counts = detect_bias(word_freq_df)

# Analyze sentiment by bias category
sentiment_by_bias = analyze_sentiment_by_bias(df, bias_lexicon)

# Convert bias counts to DataFrame
bias_df = pd.DataFrame({'Bias Category': list(bias_counts.keys()), 'Bias Count': list(bias_counts.values())})

# Convert sentiment by bias to DataFrame
sentiment_by_bias_df = pd.DataFrame.from_dict(sentiment_by_bias, orient='index').reset_index()
sentiment_by_bias_df.columns = ['Bias Category', 'Positive', 'Negative', 'Neutral']

# Save results to Excel with three sheets (Bias Analysis + Sentiment Analysis + Sentiment by Bias)
with pd.ExcelWriter(output_file) as writer:
    bias_df.to_excel(writer, sheet_name='Bias Analysis', index=False)
    sentiment_summary.to_excel(writer, sheet_name='Sentiment Analysis', index=False)
    sentiment_by_bias_df.to_excel(writer, sheet_name='Sentiment by Bias', index=False)

print(f'NBA Bias and sentiment analysis results saved to {output_file}')
