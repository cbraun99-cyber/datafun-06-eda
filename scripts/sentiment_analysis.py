import sqlite3
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

class SentimentAnalysis:
    def __init__(self, db_path='amazon_reviews.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def analyze_sentiment(self, sample_size=1000):
        """Perform sentiment analysis on review text"""
        
        print("🧠 Performing Sentiment Analysis...")
        
        # Sample reviews for analysis (to avoid processing all)
        reviews = pd.read_sql_query(f'''
            SELECT reviewText, overall, category
            FROM reviews 
            WHERE reviewText IS NOT NULL AND LENGTH(reviewText) > 10
            ORDER BY RANDOM()
            LIMIT {sample_size}
        ''', self.conn)
        
        print(f"Analyzing sentiment for {len(reviews)} reviews...")
        
        # Calculate sentiment polarity
        reviews['sentiment'] = reviews['reviewText'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        
        # Categorize sentiment
        reviews['sentiment_label'] = reviews['sentiment'].apply(
            lambda x: 'Positive' if x > 0.1 else 'Negative' if x < -0.1 else 'Neutral'
        )
        
        return reviews
    
    def sentiment_vs_rating(self, reviews):
        """Compare sentiment analysis with star ratings"""
        
        print("\n⭐ Sentiment vs Star Ratings:")
        correlation = reviews[['overall', 'sentiment']].corr().iloc[0,1]
        print(f"Correlation between rating and sentiment: {correlation:.3f}")
        
        # Plot sentiment by rating
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=reviews, x='overall', y='sentiment')
        plt.title('Sentiment Polarity by Star Rating')
        plt.xlabel('Star Rating')
        plt.ylabel('Sentiment Polarity')
        plt.tight_layout()
        plt.savefig('sentiment_vs_rating.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return correlation

if __name__ == "__main__":
    sa = SentimentAnalysis()
    reviews = sa.analyze_sentiment(500)  # Smaller sample for quick demo
    correlation = sa.sentiment_vs_rating(reviews)