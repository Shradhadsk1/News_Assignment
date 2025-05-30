# -*- coding: utf-8 -*-
"""
utils.py
"""

import requests
from textblob import TextBlob
from gtts import gTTS

API_KEY = "91ca5a7a00ff4917b03508996730f1c3"  # Replace with a valid API key


def get_news_articles(company_name):
    """Fetches news articles using NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    return [
        {"title": article["title"], "link": article["url"]}
        for article in data.get("articles", [])[:10]  # Limit to top 10 articles
    ]


def analyze_sentiment(text):
    """Performs sentiment analysis on text using TextBlob."""
    score = TextBlob(text).sentiment.polarity

    if score > 0.1:
        return "Positive"
    if score < -0.1:
        return "Negative"
    return "Neutral"


def generate_tts(text, lang="hi"):
    """Generates a Hindi text-to-speech (TTS) audio file."""
    tts = gTTS(text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    return filename


def filter_articles(articles, query):
    """Filters news articles based on a search query."""
    query = query.lower()
    return [article for article in articles if query in article["title"].lower()]


def generate_sentiment_report(sentiment_counts, articles):
    """Generates a comparative sentiment report for the fetched news articles."""
    report = "📊 **Sentiment Analysis Report:**\n\n"
    report += f"- **Positive Articles:** {sentiment_counts['Positive']}\n"
    report += f"- **Negative Articles:** {sentiment_counts['Negative']}\n"
    report += f"- **Neutral Articles:** {sentiment_counts['Neutral']}\n\n"

    # Add individual article sentiment breakdown
    report += "**📰 Comparative Sentiment Analysis Across Articles:**\n\n"
    for i, article in enumerate(articles, start=1):
        report += f"{i}. **{article['Title']}**\n"
        report += f"   - Sentiment: {article['Sentiment']}\n"
        report += f"   - 🔗 [Read More]({article['Link']})\n\n"

    return report
