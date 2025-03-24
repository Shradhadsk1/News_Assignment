# News Sentiment Analysis API

## Overview
This project is a **News Sentiment Analysis API** that fetches news articles about a given company, analyzes the sentiment of the news, and provides insights into how the company's news coverage varies. Additionally, it generates a summarized audio report in Hindi using text-to-speech (TTS). The API is developed using **FastAPI** and deployed on **Hugging Face Spaces**.

## Features
- Fetches latest news articles related to a given company using **NewsAPI**.
- Performs **sentiment analysis** on the news articles.
- Extracts key **topics** from the articles.
- Provides a **comparative sentiment analysis**.
- Generates a **Hindi audio summary** of the sentiment analysis.
- Offers a **RESTful API** for querying and retrieving results.

## File Structure
```
├── app.py                # Main FastAPI application
├── api.py                # API routes and endpoints
├── utils.py              # Utility functions (news fetching, sentiment analysis, etc.)
├── requirements.txt      # Required dependencies for the project
```

## Setup and Installation
### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/news-sentiment-analysis.git
cd news-sentiment-analysis
```

### 2. Install Dependencies
Ensure you have Python installed (preferably 3.8+), then run:
```sh
pip install -r requirements.txt
```

### 3. Set Up API Key
Replace the `API_KEY` in `utils.py` with your **NewsAPI** key:
```python
API_KEY = "your_newsapi_key_here"
```

### 4. Run the FastAPI Application
```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Your API will be accessible at `http://127.0.0.1:8000`.

### 5. Test the API
You can use the built-in **Swagger UI** to test endpoints:
```sh
http://127.0.0.1:8000/docs
```
Or use **cURL/Postman**:
```sh
curl -X 'GET' 'http://127.0.0.1:8000/news/sentiment?company=Tesla' -H 'accept: application/json'
```

## API Endpoints
### 1. Fetch News and Analyze Sentiment
**Endpoint:** `/news/sentiment`
- **Method:** `GET`
- **Parameters:**
  - `company` (string, required) → Name of the company.
- **Response:**
```json
{
  "company": "Tesla",
  "articles": [
    {"title": "Tesla hits record sales", "sentiment": "Positive", "topics": ["sales", "growth"]},
    {"title": "Tesla faces lawsuit", "sentiment": "Negative", "topics": ["lawsuit", "legal issues"]}
  ],
  "comparative_analysis": "Tesla has mixed coverage with both growth and legal issues discussed."
}
```

### 2. Get Hindi Audio Summary
**Endpoint:** `/news/audio_summary`
- **Method:** `GET`
- **Parameters:**
  - `company` (string, required) → Name of the company.
- **Response:**
Returns an MP3 file with a Hindi audio summary.

## Deployment on Hugging Face Spaces
To deploy on Hugging Face:
1. Create a **new Space** on Hugging Face.
2. Upload all project files (`app.py`, `api.py`, `utils.py`, `requirements.txt`).
3. Set up the `requirements.txt` to install dependencies.
4. Start the Space and test the API.

## Dependencies
The project requires the following dependencies (defined in `requirements.txt`):
```txt

fastapi==0.95.0
uvicorn==0.23.2
requests==2.28.1
textblob==0.17.1
gtts==2.3.2
beautifulsoup4==4.11.1
gradio==3.50.2
pydantic==1.10.7

```

## Future Enhancements
- Improve topic extraction using **NLP models**.
- Add **multilingual support** for text and audio summaries.
- Implement **real-time news tracking**.

## License
This project is open-source and available under the **MIT License**.

---
For any issues, feel free to raise an issue on GitHub! 🚀

