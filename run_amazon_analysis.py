import os
import sys

def main():
    """Main execution script for Amazon Reviews Analysis"""
    
    print("🛍️ AMAZON PRODUCT REVIEWS ANALYSIS")
    print("="*50)
    
    # Check if data exists
    if not os.path.exists('data/amazon_reviews_electronics.csv'):
        print("📥 Downloading Amazon dataset...")
        from data.download_amazon import download_amazon_data
        download_amazon_data()
        
        if not os.path.exists('data/amazon_reviews_electronics.csv'):
            print("❌ Download failed. Please check manual download instructions.")
            return
    
    # Initialize database
    print("🗃️ Initializing database...")
    from scripts.init_database import initialize_amazon_database
    if not initialize_amazon_database():
        return
    
    # Run main EDA
    print("📊 Running EDA analysis...")
    from scripts.amazon_eda import AmazonEDA
    eda = AmazonEDA()
    eda.generate_report()
    
    # Run sentiment analysis (optional)
    try:
        print("\n🧠 Running sentiment analysis...")
        from scripts.sentiment_analysis import SentimentAnalysis
        sa = SentimentAnalysis()
        reviews = sa.analyze_sentiment(500)
        sa.sentiment_vs_rating(reviews)
    except ImportError:
        print("❌ TextBlob not installed. Skipping sentiment analysis.")
        print("💡 Run: pip install textblob && python -m textblob.download_corpora")
    
    print("\n✅ Analysis complete!")
    print("📈 Check generated files:")
    print("   - amazon_analysis_dashboard.png")
    print("   - sentiment_vs_rating.png (if sentiment analysis ran)")

if __name__ == "__main__":
    main()