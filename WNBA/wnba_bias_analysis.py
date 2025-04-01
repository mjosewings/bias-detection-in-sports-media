import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


# Define Bias Lexicon
bias_lexicon = {
    "physicality_bias": ["strong", "aggressive", "dominant", "athletic", "big",
                         "tall", "heavy", "giraffe", "lurch", "gangly", "clumsy",
                         "graceful", "fragile", "delicate", "feminine", "nimble", "powerful",
                         "muscular", "toned", "weak", "fragile", "dainty", "delicate", "skinny"],

    "emotional_bias": ["emotional", "graceful", "lucky", "passionate", "whiney",
                       "sensitive", "overemotional", "soft", "fragile", "hysterical",
                       "bitchy", "hormonal", "volatile", "irrational", "delusional",
                       "melodramatic", "unstable", "irrational"],

    "diminishing_bias": ["surprisingly good", "plays like a man", "given an opportunity",
                         "fortunate", "underdog", "lucky", "not as good as expected",
                         "plays above her station", "unexpected success", "hidden gem",
                         "overachiever", "too emotional to succeed", "not expected to do well"],

    "success_bias": ["earned it", "proved himself", "fortunate", "gifted", "lucky",
                     "passionate", "best", "deserved", "grinder", "hard worker",
                     "overcame the odds", "proven", "elite", "underdog story",
                     "underestimated", "scrappy", "tenacious", "determined",
                     "self-made", "underdog turned star"],

    "class_bias": ["classless", "ghetto", "trash", "low class", "immature", "bully",
                   "brat", "spoiled", "horrible", "humble", "pride", "ego", "devil",
                   "loser", "trash talk", "taunt", "punk", "scumbag", "ashamed",
                   "delusional", "arrogant", "disrespect", "idiot", "stupid", "schoolyard",
                   "thug", "classy", "nasty", "clown", "foolish", "ignorance", "pathetic",
                   "disgrace", "ungrateful", "virtue", "sportsmanship", "grace", "integrity",
                   "dignity", "lowlife", "shrink", "wannabe", "haughty", "selfish", "conceit",
                   "embarrassing", "screaming", "viral", "scum", "sad", "laughable", "bitch",
                   "moving", "shameful", "lowborn", "unpolished", "uncouth", "unrefined",
                   "embarrassing", "ghetto fabulous", "loud", "uneducated", "unclassy"],

    "racial_bias": ["black", "white", "racist", "negro", "hood", "woke", "color", "separation",
                    "inclusion", "privilege", "antiwhiteism", "card", "ghetto", "thug",
                    "lazy", "angry", "unprofessional", "privileged", "entitled", "ungrateful",
                    "unrefined", "insecure", "savage", "hostile", "aggressive", "ungrateful",
                    "hyperactive", "disruptive", "too loud", "overstepping", "unpolished",
                    "unfeminine", "scary", "uneducated", "out of control"],

    "skill_bias": ["talent", "skill", "better", "outplayed", "average", "weak", "worst",
                   "mediocre", "gift", "lack", "genius", "goat", "best", "exceptional",
                   "superior", "flawless", "elite", "outstanding", "underperforming",
                   "misused", "underappreciated", "underestimated", "not up to par",
                   "underachiever", "exceptional"],

    "appearance_bias": ["beautiful", "gross", "sweaty", "armpit", "hair", "sewed", "wig",
                        "makeup", "fake", "eyelash", "dress", "big mouth", "pretty", "cute",
                        "unattractive", "hairy", "nappy", "dolled", "unpolished", "rough",
                        "unfeminine", "overdone", "unmade", "tacky", "heavyset", "plain",
                        "disheveled", "scruffy", "untidy", "unrefined", "unattractive",
                        "unappealing", "dull", "awkward", "ugly", "clumsy", "exaggerated"],

    "gender/sexuality_bias": ["woman", "girl", "female", "lesbian", "man", "Plays like a man",
                             "sissy", "butch", "queer", "dike", "feminine", "overly emotional",
                             "too masculine", "tomboy", "whiney", "hyper-feminine", "gender-fluid",
                             "unladylike", "effeminate", "masculine", "dominant", "sexualized",
                             "over-sexualized", "over-compensating", "stereotypical", "hyper-masculine",
                             "unmanly", "trans", "drag queen", "lesbian stereotype", "femme", "bisexual"],

    "age_bias": ["old", "young", "baby", "immature", "childish", "first grader", "schoolyard",
                 "toddler", "year old", "yrs old", "young lady", "whiney", "juvenile", "senile",
                 "past their prime", "young and naive", "over the hill", "old fashioned",
                 "not young anymore", "over the hill", "young-at-heart", "aging", "youngin"],

    "disability_bias": ["whiney", "crippled", "handicapped", "broken", "impaired", "dependent",
                        "weak", "incapacitated", "defective", "unable", "disabled", "invalid",
                        "wheelchair-bound", "slow", "retarded", "imperfect", "mentally challenged",
                        "special", "fragile", "different", "physically challenged", "slow",
                        "sick", "disabling", "incapacitated", "helpless", "incapable"],

    "sexuality_bias": ["lesbian", "bisexual", "gay", "queer", "straight", "heterosexual",
                       "homophobic", "coming out", "pride", "LGBTQ", "drag queen", "gender fluid",
                       "gay agenda", "gender nonconforming", "queer identity", "openly gay",
                       "homosexual", "transgender", "lesbian stereotype", "pansexual",
                       "fluid", "bi-curious", "homosexual agenda", "straight acting", "butch",
                       "femme", "non-binary", "overly sexual", "heteronormative", "heterosexist",
                       "sexual orientation", "unfaithful", "attracted to women", "attracted to men",
                       "predatory", "sexual deviance", "sensitive", "effeminate"],

    "nationality_bias": ["American", "foreign", "un-American", "patriot", "foreign-born",
                         "immigrant", "illegal", "alien", "outsider", "refugee", "displaced",
                         "third-world", "western", "eastern", "nationalist", "unpatriotic",
                         "anti-American", "xenophobic", "American dream", "subhuman", "low-born",
                         "other", "non-American", "undocumented", "national pride", "nationalist",
                         "multicultural", "ethnic", "cultural appropriation", "anti-immigrant",
                         "foreigner", "anti-foreign", "exotic", "outsider", "native", "unwelcome"],

    "team_affiliation_bias": ["bandwagon", "glory hunter", "loyal fan", "fairweather fan",
                              "diehard fan", "newbie", "jumping ship", "underdog", "jumping on the bandwagon",
                              "front-runner", "losing streak", "cheering for the winner", "bandwagoner",
                              "fairweather fan", "loyal to the team", "plastic fan", "unpredictable fanbase",
                              "supporting the winning team", "popular team", "underdog team", "fairweather supporter",
                              "committed fan", "seasonal fan", "non-local fan", "hipster fan", "casual fan",
                              "dedicated fan", "loyalist", "no-nonsense fan", "casual observer", "fairweather follower"]
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
input_file = 'The_Day_Caitlin_Clark_Showed_Angel_Reese_Who’s_Boss_comments.txt'
output_file = 'wnba_analysis_sentiment_results.xlsx'

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

print(f'WNBA Bias and sentiment analysis results saved to {output_file}')
