# Cryptocurrency Sentiment Analysis

This project analyzes public sentiment towards major cryptocurrencies by collecting and analyzing Reddit posts. It provides an interactive dashboard to visualize sentiment trends and post volumes over time.

## Features

- Collects cryptocurrency-related posts from multiple Reddit subreddits
- Performs sentiment analysis using NLTK's VADER
- Interactive Streamlit dashboard with:
  - Sentiment trends over time
  - Post volume analysis
  - Sentiment distribution visualization
  - Top posts display
- Support for multiple cryptocurrencies
- Customizable date range selection

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd crypto_sentiment_analysis
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

To get Reddit API credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Fill in the required information
4. Select "script" as the app type
5. Copy the client ID and client secret

## Usage

1. Start the Streamlit dashboard:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar to:
   - Select a cryptocurrency
   - Choose a date range
   - Click "Analyze Sentiment" to start the analysis

## Project Structure

- `app.py`: Streamlit dashboard implementation
- `scraper.py`: Reddit data collection module
- `sentiment_analyzer.py`: Sentiment analysis implementation
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create this file with your Reddit API credentials)

## Dependencies

- praw: Reddit API wrapper
- pandas: Data manipulation
- nltk: Natural language processing and sentiment analysis
- streamlit: Interactive dashboard
- plotly: Data visualization
- python-dotenv: Environment variable management

## Contributing

Feel free to submit issues and enhancement requests!