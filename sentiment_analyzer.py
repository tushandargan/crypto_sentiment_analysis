import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text):
        """
        Analyze the sentiment of a given text using VADER.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Dictionary containing sentiment scores
        """
        if not isinstance(text, str) or not text.strip():
            return {'compound': 0, 'pos': 0, 'neu': 0, 'neg': 0}
        
        return self.sia.polarity_scores(text)
    
    def analyze_posts(self, posts_df):
        """
        Analyze sentiment for a DataFrame of posts.
        
        Args:
            posts_df (pd.DataFrame): DataFrame containing posts with 'title' and 'text' columns
            
        Returns:
            pd.DataFrame: DataFrame with added sentiment scores
        """
        # Create a copy to avoid modifying the original
        df = posts_df.copy()
        
        # Analyze title sentiment
        df['title_sentiment'] = df['title'].apply(self.analyze_text)
        df['title_compound'] = df['title_sentiment'].apply(lambda x: x['compound'])
        
        # Analyze text sentiment
        df['text_sentiment'] = df['text'].apply(self.analyze_text)
        df['text_compound'] = df['text_sentiment'].apply(lambda x: x['compound'])
        
        # Calculate overall sentiment (weighted average of title and text)
        df['overall_sentiment'] = (df['title_compound'] * 0.4 + df['text_compound'] * 0.6)
        
        return df
    
    def get_sentiment_summary(self, analyzed_df):
        """
        Generate summary statistics for the sentiment analysis.
        
        Args:
            analyzed_df (pd.DataFrame): DataFrame with sentiment scores
            
        Returns:
            dict: Dictionary containing sentiment summary statistics
        """
        return {
            'mean_sentiment': analyzed_df['overall_sentiment'].mean(),
            'median_sentiment': analyzed_df['overall_sentiment'].median(),
            'std_sentiment': analyzed_df['overall_sentiment'].std(),
            'positive_posts': len(analyzed_df[analyzed_df['overall_sentiment'] > 0]),
            'negative_posts': len(analyzed_df[analyzed_df['overall_sentiment'] < 0]),
            'neutral_posts': len(analyzed_df[analyzed_df['overall_sentiment'] == 0]),
            'total_posts': len(analyzed_df)
        } 