import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scraper import RedditScraper
from sentiment_analyzer import SentimentAnalyzer

# Set page config
st.set_page_config(
    page_title="Crypto Sentiment Analysis",
    page_icon="📈",
    layout="wide"
)

# Initialize components
scraper = RedditScraper()
analyzer = SentimentAnalyzer()

# Title and description
st.title("Cryptocurrency Sentiment Analysis")
st.markdown("""
This dashboard analyzes public sentiment towards cryptocurrencies by collecting and analyzing Reddit posts.
Select a cryptocurrency and date range to see the sentiment analysis results.
""")

# Sidebar inputs
st.sidebar.header("Analysis Parameters")

# Cryptocurrency selection
crypto_options = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum',
    'Cardano': 'cardano',
    'Solana': 'solana',
    'Polkadot': 'polkadot'
}
selected_crypto = st.sidebar.selectbox(
    "Select Cryptocurrency",
    list(crypto_options.keys())
)

# Date range selection
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(start_date, end_date),
    max_value=end_date
)

# Analysis button
if st.sidebar.button("Analyze Sentiment"):
    with st.spinner("Collecting and analyzing data..."):
        # Get posts
        posts_df = scraper.get_crypto_posts(
            crypto_options[selected_crypto],
            datetime.combine(date_range[0], datetime.min.time()),
            datetime.combine(date_range[1], datetime.max.time())
        )
        
        if len(posts_df) == 0:
            st.error("No posts found for the selected parameters. Try adjusting the date range or cryptocurrency.")
        else:
            # Analyze sentiment
            analyzed_df = analyzer.analyze_posts(posts_df)
            sentiment_summary = analyzer.get_sentiment_summary(analyzed_df)
            
            # Display summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Sentiment", f"{sentiment_summary['mean_sentiment']:.2f}")
            with col2:
                st.metric("Total Posts", sentiment_summary['total_posts'])
            with col3:
                st.metric("Positive Posts", sentiment_summary['positive_posts'])
            with col4:
                st.metric("Negative Posts", sentiment_summary['negative_posts'])
            
            # Sentiment over time
            st.subheader("Sentiment Over Time")
            daily_sentiment = analyzed_df.groupby(analyzed_df['created_utc'].dt.date)['overall_sentiment'].mean().reset_index()
            fig = px.line(daily_sentiment, x='created_utc', y='overall_sentiment',
                         title=f"Daily Average Sentiment for {selected_crypto}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Post volume over time
            st.subheader("Post Volume Over Time")
            daily_volume = analyzed_df.groupby(analyzed_df['created_utc'].dt.date).size().reset_index(name='count')
            fig = px.bar(daily_volume, x='created_utc', y='count',
                        title=f"Daily Post Volume for {selected_crypto}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Sentiment distribution
            st.subheader("Sentiment Distribution")
            fig = px.histogram(analyzed_df, x='overall_sentiment',
                             title=f"Distribution of Sentiment Scores for {selected_crypto}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Display top posts
            st.subheader("Top Posts")
            top_posts = analyzed_df.nlargest(5, 'overall_sentiment')
            for _, post in top_posts.iterrows():
                with st.expander(f"Score: {post['overall_sentiment']:.2f} - {post['title']}"):
                    st.write(post['text'])
                    st.write(f"Subreddit: r/{post['subreddit']}")
                    st.write(f"Posted on: {post['created_utc'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"Upvotes: {post['score']} | Comments: {post['num_comments']}")

# Footer
st.markdown("---")
st.markdown("Data collected from Reddit using PRAW. Sentiment analysis performed using NLTK's VADER.")
