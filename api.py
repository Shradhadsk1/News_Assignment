# -*- coding: utf-8 -*-
"""api.py
"""

import requests
from textblob import TextBlob
from gtts import gTTS
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pyngrok import ngrok
import nest_asyncio

# Allow event loop to run inside Jupyter/Colab
nest_asyncio.apply()

# Initialize FastAPI app
app = FastAPI()

# Replace this with a valid API key
API_KEY = "91ca5a7a00ff4917b03508996730f1c3"


def get_news_articles(company_name: str):
    """
    Fetches the latest news articles for a given company using NewsAPI.
    """
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching news articles"
        )

    data = response.json()
    articles = [
        {"title": article["title"], "link": article["url"]}
        for article in data.get("articles", [])[:10]
    ]
    return articles


def analyze_sentiment(text: str) -> str:
    """
    Performs sentiment analysis on text using TextBlob.
    Returns 'Positive', 'Negative', or 'Neutral'.
    """
    score = TextBlob(text).sentiment.polarity
    if score > 0.1:
        return "Positive"
    if score < -0.1:
        return "Negative"
    return "Neutral"


def generate_tts(text: str, lang: str = "hi") -> str:
    """
    Generates a Hindi text-to-speech (TTS) audio file from text.
    Returns the filename of the generated audio.
    """
    tts = gTTS(text, lang=lang)
    filename = "output.mp3"
    tts.save(filename)
    return filename


def filter_articles(articles: list, query: str) -> list:
    """
    Filters news articles based on a search query.
    """
    query = query.lower()
    return [article for article in articles if query in article["title"].lower()]


def generate_sentiment_report(sentiment_counts: dict, articles: list) -> str:
    """
    Generates a detailed sentiment analysis report for the fetched news articles.
    """
    report = "📊 **Sentiment Analysis Report:**\n\n"
    report += f"- **Positive Articles:** {sentiment_counts['Positive']}\n"
    report += f"- **Negative Articles:** {sentiment_counts['Negative']}\n"
    report += f"- **Neutral Articles:** {sentiment_counts['Neutral']}\n\n"
    report += "**📰 Comparative Sentiment Analysis Across Articles:**\n\n"

    for i, article in enumerate(articles, start=1):
        report += f"{i}. **{article['Title']}**\n"
        report += f"   - Sentiment: {article['Sentiment']}\n"
        report += f"   - 🔗 [Read More]({article['Link']})\n\n"
    
    return report


class NewsRequest(BaseModel):
    """
    Pydantic model for news request payload.
    """
    company_name: str
    query: str = ""


@app.get("/news/{company_name}")
def get_news(company_name: str):
    """
    API Endpoint to fetch news articles for a company.
    """
    articles = get_news_articles(company_name)
    return {"company": company_name, "articles": articles}


@app.post("/fetch-news/")
def fetch_news(request: NewsRequest):
    """
    API Endpoint to fetch news articles, perform sentiment analysis, and generate a report.
    Optionally filters articles based on a search query.
    """
    articles = get_news_articles(request.company_name)
    
    if not articles:
        return {"message": "No news articles found."}

    filtered_articles = (
        filter_articles(articles, request.query) if request.query else articles
    )
    
    if not filtered_articles:
        return {"message": f"No articles found related to '{request.query}'."}

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    processed_articles = []

    for article in filtered_articles:
        sentiment = analyze_sentiment(article["title"])
        sentiment_counts[sentiment] += 1
        processed_articles.append({
            "Title": article["title"],
            "Sentiment": sentiment,
            "Link": article["link"]
        })

    sentiment_report = generate_sentiment_report(sentiment_counts, processed_articles)

    return {
        "company": request.company_name,
        "total_articles": len(filtered_articles),
        "sentiment_counts": sentiment_counts,
        "sentiment_report": sentiment_report,
        "articles": processed_articles
    }


@app.post("/generate-tts/")
def generate_tts_audio(company_name: str):
    """
    API Endpoint to generate a Hindi text-to-speech audio summary.
    """
    summary = f"{company_name} के बारे में समाचार विश्लेषण उपलब्ध है।"
    audio_file = generate_tts(summary, lang="hi")
    return {"message": "TTS audio generated successfully", "audio_file": audio_file}


# Expose API to the internet using ngrok
public_url = ngrok.connect(8000).public_url
print(f"🚀 Public URL: {public_url}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
