import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

# Bias Detection Function
def detect_bias(word_freq_df):
    # Initialize bias count dictionary
    bias_counts = {bias_category: 0 for bias_category in bias_lexicon}

    # Iterate through the lexicon and count occurrences
    for bias_category, keywords in bias_lexicon.items():
        for word in keywords:
            if word in word_freq_df['word'].values:
                # Sum the frequency of words in the dataframe
                bias_counts[bias_category] += word_freq_df[word_freq_df['word'] == word]['frequency'].sum()

    return bias_counts


# Sentiment Analysis Function
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    return sentiment_score['compound']  # Returns the compound score


# Load the dataset
input_csv = 'The_Day_Caitlin_Clark_Showed_Angel_Reese_Who’s_Boss_comments.txt'
output_csv = 'wnba_analysis_results.csv'

# Read the CSV file
df = pd.read_csv(input_csv)

# Perform sentiment analysis on each article
df['sentiment'] = df['content'].apply(analyze_sentiment)

# Tokenize and create word frequency dataframe
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(stop_words='english')
word_freq_matrix = vectorizer.fit_transform(df['content'])

# Convert word frequency matrix to dataframe
word_freq_df = pd.DataFrame(word_freq_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Perform bias detection on the articles
bias_counts = detect_bias(word_freq_df)

# Create a DataFrame to store the results
analysis_df = pd.DataFrame({'Bias Category': list(bias_counts.keys()),
                            'Bias Count': list(bias_counts.values())})

# Save the analysis results to a CSV file
analysis_df.to_csv(output_csv, index=False)

print(f'Bias and sentiment analysis results saved to {output_csv}')
