import sqlite3
import pandas as pd
import os
import glob
import json

def initialize_amazon_database():
    """Initialize SQLite database with Amazon data"""
    
    # Check for data files
    review_files = glob.glob('data/amazon_reviews_*.csv')
    product_files = glob.glob('data/amazon_products_*.csv')
    
    if not review_files:
        print("❌ No review data found! Run download_amazon.py first.")
        return False
    
    print("📊 Initializing Amazon Database...")
    
    # Create database
    conn = sqlite3.connect('amazon_reviews.db')
    
    # Load reviews data
    all_reviews = []
    for file in review_files:
        category = file.split('_')[-1].replace('.csv', '')
        print(f"Loading {category} reviews...")
        
        df = pd.read_csv(file)
        df['category'] = category
        all_reviews.append(df)
    
    # Combine all reviews
    reviews_df = pd.concat(all_reviews, ignore_index=True)
    reviews_df.to_sql('reviews', conn, if_exists='replace', index=False)
    print(f"✅ Loaded {len(reviews_df):,} total reviews")
    
    # Load product data if available
    if product_files:
        all_products = []
        for file in product_files:
            category = file.split('_')[-1].replace('.csv', '')
            print(f"Loading {category} products...")
            
            df = pd.read_csv(file)
            df['category'] = category
            all_products.append(df)
        
        products_df = pd.concat(all_products, ignore_index=True)
        products_df.to_sql('products', conn, if_exists='replace', index=False)
        print(f"✅ Loaded {len(products_df):,} products")
    
    # Create indexes
    cursor = conn.cursor()
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_reviews_asin ON reviews(asin);",
        "CREATE INDEX IF NOT EXISTS idx_reviews_overall ON reviews(overall);",
        "CREATE INDEX IF NOT EXISTS idx_reviews_category ON reviews(category);",
        "CREATE INDEX IF NOT EXISTS idx_products_asin ON products(asin);"
    ]
    
    for index_sql in indexes:
        try:
            cursor.execute(index_sql)
        except Exception as e:
            print(f"Index error: {e}")
    
    conn.commit()
    
    # Display database stats
    print("\n📋 Database Summary:")
    tables = ['reviews', 'products']
    for table in tables:
        try:
            count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0,0]
            print(f"   {table}: {count:,} records")
        except:
            print(f"   {table}: not found")
    
    # Sample data preview
    print("\n🔍 Sample Review Data:")
    sample = pd.read_sql_query("SELECT * FROM reviews LIMIT 3", conn)
    print(sample[['asin', 'overall', 'category', 'reviewText']].head(3))
    
    conn.close()
    return True

def explore_data_quality():
    """Explore data quality and basic statistics"""
    
    conn = sqlite3.connect('amazon_reviews.db')
    
    print("\n📈 Data Quality Report:")
    print("="*50)
    
    # Review statistics
    review_stats = pd.read_sql_query('''
        SELECT 
            COUNT(*) as total_reviews,
            COUNT(DISTINCT asin) as unique_products,
            COUNT(DISTINCT reviewerID) as unique_reviewers,
            AVG(overall) as avg_rating,
            MIN(overall) as min_rating,
            MAX(overall) as max_rating
        FROM reviews
    ''', conn)
    
    print("Review Statistics:")
    for col in review_stats.columns:
        print(f"   {col}: {review_stats.iloc[0][col]}")
    
    # Rating distribution
    rating_dist = pd.read_sql_query('''
        SELECT 
            overall as rating,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) as percentage
        FROM reviews
        GROUP BY overall
        ORDER BY overall
    ''', conn)
    
    print("\nRating Distribution:")
    print(rating_dist.to_string(index=False))
    
    # Category distribution
    category_dist = pd.read_sql_query('''
        SELECT 
            category,
            COUNT(*) as review_count,
            COUNT(DISTINCT asin) as product_count,
            AVG(overall) as avg_rating
        FROM reviews
        GROUP BY category
        ORDER BY review_count DESC
    ''', conn)
    
    print("\nCategory Distribution:")
    print(category_dist.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    if initialize_amazon_database():
        explore_data_quality()