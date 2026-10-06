from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


# Download VADER lexicon if it is not already available
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)

    compound_score = scores["compound"]

    if compound_score >= 0.05:
        sentiment = "Positive"

    elif compound_score <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, compound_score


if __name__ == "__main__":

    test_feedback = [
        "The product is excellent and I am very happy.",
        "The product is okay.",
        "Very bad experience. I am disappointed."
    ]

    for feedback in test_feedback:

        sentiment, score = analyze_sentiment(feedback)

        print("Feedback:", feedback)
        print("Sentiment:", sentiment)
        print("Score:", score)
        print("-" * 40)