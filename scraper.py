import praw
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
    def get_crypto_posts(self, coin_name, start_date, end_date, subreddits=['cryptocurrency', 'CryptoMarkets', 'CryptoCurrency']):
        """
        Collect posts related to a specific cryptocurrency from specified subreddits
        within a given date range.
        
        Args:
            coin_name (str): Name of the cryptocurrency (e.g., 'bitcoin', 'ethereum')
            start_date (datetime): Start date for the search
            end_date (datetime): End date for the search
            subreddits (list): List of subreddits to search in
            
        Returns:
            pd.DataFrame: DataFrame containing the collected posts
        """
        posts = []
        
        for subreddit_name in subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Search for posts containing the coin name
            search_query = f"{coin_name}"
            for submission in subreddit.search(search_query, sort='relevance', time_filter='all'):
                post_date = datetime.fromtimestamp(submission.created_utc)
                
                # Check if post is within date range
                if start_date <= post_date <= end_date:
                    post_data = {
                        'title': submission.title,
                        'text': submission.selftext,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': post_date,
                        'subreddit': subreddit_name,
                        'url': submission.url,
                        'author': str(submission.author),
                        'id': submission.id
                    }
                    posts.append(post_data)
        
        return pd.DataFrame(posts)

    def get_comments(self, post_id):
        """
        Collect all comments for a specific post.
        
        Args:
            post_id (str): Reddit post ID
            
        Returns:
            pd.DataFrame: DataFrame containing the comments
        """
        submission = self.reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # Remove MoreComments objects
        
        comments = []
        for comment in submission.comments.list():
            comment_data = {
                'text': comment.body,
                'score': comment.score,
                'created_utc': datetime.fromtimestamp(comment.created_utc),
                'author': str(comment.author),
                'parent_id': comment.parent_id
            }
            comments.append(comment_data)
            
        return pd.DataFrame(comments)
