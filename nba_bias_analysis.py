import pandas as pd
import re

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


# Bias Detection Function
def detect_bias(word_freq_df):
    # Initialize bias count dictionary
    bias_counts = {category: 0 for category in bias_lexicon}

    # Iterate through bias categories and words
    for category, words in bias_lexicon.items():
        for word in words:
            if word in word_freq_df.index:  # Check if word exists in frequency data
                bias_counts[category] += word_freq_df.at[word, 'Frequency']

    # Total bias occurrences
    bias_counts["total_bias_count"] = sum(bias_counts.values())

    return bias_counts


# Load word frequency data from NBA CSV file
input_csv = 'nba_word_frequencies.csv'  # Update this with the correct filename
word_freq_df = pd.read_csv(input_csv)

# Ensure words are the index
word_freq_df.set_index("Word", inplace=True)

# Detect bias in the word frequency data
bias_results = detect_bias(word_freq_df)

# Convert bias results to DataFrame
bias_df = pd.DataFrame([bias_results])

# Save to New CSV
output_csv = 'nba_bias_analysis.csv'
bias_df.to_csv(output_csv, index=False)

print(f"NBA Bias analysis results saved to {output_csv}")
