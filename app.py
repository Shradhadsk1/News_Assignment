import gradio as gr

def fetch_and_process_news(company_name: str, query: str = ""):
    """
    Fetch news articles, analyze sentiment, and allow users to search for specific topics.
    Includes comparative sentiment analysis.
    """
    articles = get_news_articles(company_name)

    if not articles:
        return "कोई समाचार लेख नहीं मिला।", None  # No articles found message in Hindi

    # Apply filtering based on query (if provided)
    filtered_articles = filter_articles(articles, query) if query else articles

    if not filtered_articles:
        return f"कोई लेख '{query}' से संबंधित नहीं मिला।", None  # No articles matching query

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    processed_articles = []

    # Perform sentiment analysis and collect article details
    results = []
    for article in filtered_articles:
        sentiment = analyze_sentiment(article["title"])
        sentiment_counts[sentiment] += 1
        processed_articles.append({
            "Title": article["title"],
            "Sentiment": sentiment,
            "Link": article["link"]
        })
        results.append(
            f"📰 {article['title']} | Sentiment: {sentiment} | [Read More]({article['link']})"
        )

    # Generate comparative sentiment report
    sentiment_report = generate_sentiment_report(sentiment_counts, processed_articles)

    # Create a detailed Hindi summary including sentiment analysis
    hindi_summary = (
        f"{company_name} के बारे में {len(filtered_articles)} समाचार लेख मिले। "
        f"{sentiment_counts['Positive']} सकारात्मक, "
        f"{sentiment_counts['Negative']} नकारात्मक, और "
        f"{sentiment_counts['Neutral']} तटस्थ लेख हैं।"
    )

    audio_file = generate_tts(hindi_summary, lang="hi")  # Generate Hindi speech output

    return sentiment_report, audio_file

# Creating Gradio UI
iface = gr.Interface(
    fn=fetch_and_process_news,
    inputs=["text", "text"],  # Second input for topic-based filtering
    outputs=["text", "audio"],
    title="📰 News Summarization & Comparative Sentiment Analysis",
    description=(
        "Enter a company name to fetch news, analyze sentiment, "
        "compare news coverage, and search specific topics."
    )
)

# Launch Gradio
iface.launch(share=True)
