import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AmazonEDA:
    def __init__(self, db_path='amazon_reviews.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def basic_overview(self):
        """Basic overview of the Amazon dataset"""
        print("🛍️ AMAZON PRODUCT REVIEWS ANALYSIS")
        print("="*60)
        
        # Basic statistics
        stats = pd.read_sql_query('''
            SELECT 
                COUNT(*) as total_reviews,
                COUNT(DISTINCT asin) as unique_products,
                COUNT(DISTINCT reviewerID) as unique_reviewers,
                AVG(overall) as avg_rating,
                MIN(unixReviewTime) as first_review,
                MAX(unixReviewTime) as last_review
            FROM reviews
        ''', self.conn)
        
        print("📊 Dataset Overview:")
        print(f"   Total Reviews: {stats.iloc[0]['total_reviews']:,}")
        print(f"   Unique Products: {stats.iloc[0]['unique_products']:,}")
        print(f"   Unique Reviewers: {stats.iloc[0]['unique_reviewers']:,}")
        print(f"   Average Rating: {stats.iloc[0]['avg_rating']:.2f}/5.0")
        
        # Convert Unix timestamps to dates
        first_date = datetime.fromtimestamp(stats.iloc[0]['first_review']).strftime('%Y-%m-%d')
        last_date = datetime.fromtimestamp(stats.iloc[0]['last_review']).strftime('%Y-%m-%d')
        print(f"   Review Period: {first_date} to {last_date}")
    
    def rating_analysis(self):
        """Analyze rating patterns and distributions"""
        print("\n⭐ RATING ANALYSIS")
        print("="*60)
        
        # Rating distribution
        rating_dist = pd.read_sql_query('''
            SELECT 
                overall as rating,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) as percentage
            FROM reviews
            GROUP BY overall
            ORDER BY overall DESC
        ''', self.conn)
        
        print("Rating Distribution:")
        for _, row in rating_dist.iterrows():
            stars = '★' * int(row['rating']) + '☆' * (5 - int(row['rating']))
            print(f"   {stars} ({row['rating']}): {row['count']:,} reviews ({row['percentage']}%)")
        
        # Rating trends over time
        monthly_ratings = pd.read_sql_query('''
            SELECT 
                strftime('%Y-%m', datetime(unixReviewTime, 'unixepoch')) as month,
                AVG(overall) as avg_rating,
                COUNT(*) as review_count
            FROM reviews
            GROUP BY month
            HAVING review_count >= 10
            ORDER BY month
        ''', self.conn)
        
        print(f"\nMonthly Rating Trends ({len(monthly_ratings)} months):")
        print(f"   Average rating range: {monthly_ratings['avg_rating'].min():.2f} - {monthly_ratings['avg_rating'].max():.2f}")
        
        return rating_dist, monthly_ratings
    
    def product_analysis(self):
        """Analyze product review patterns"""
        print("\n📦 PRODUCT ANALYSIS")
        print("="*60)
        
        # Products with most reviews
        top_products = pd.read_sql_query('''
            SELECT 
                asin,
                COUNT(*) as review_count,
                AVG(overall) as avg_rating,
                COUNT(DISTINCT reviewerID) as unique_reviewers
            FROM reviews
            GROUP BY asin
            HAVING review_count >= 5
            ORDER BY review_count DESC
            LIMIT 10
        ''', self.conn)
        
        print("Top 10 Most Reviewed Products:")
        for i, (_, row) in enumerate(top_products.iterrows(), 1):
            print(f"   {i}. Product {row['asin']}: {row['review_count']} reviews, {row['avg_rating']:.2f} avg rating")
        
        # Review distribution per product
        product_stats = pd.read_sql_query('''
            SELECT 
                COUNT(*) as product_count,
                AVG(review_count) as avg_reviews_per_product,
                MAX(review_count) as max_reviews
            FROM (
                SELECT asin, COUNT(*) as review_count
                FROM reviews
                GROUP BY asin
            )
        ''', self.conn)
        
        print(f"\nProduct Review Statistics:")
        print(f"   Average reviews per product: {product_stats.iloc[0]['avg_reviews_per_product']:.1f}")
        print(f"   Maximum reviews for one product: {product_stats.iloc[0]['max_reviews']}")
        
        return top_products, product_stats
    
    def reviewer_analysis(self):
        """Analyze reviewer behavior"""
        print("\n👥 REVIEWER ANALYSIS")
        print="="*60)
        
        # Most active reviewers
        top_reviewers = pd.read_sql_query('''
            SELECT 
                reviewerID,
                COUNT(*) as review_count,
                AVG(overall) as avg_rating,
                MIN(unixReviewTime) as first_review,
                MAX(unixReviewTime) as last_review
            FROM reviews
            GROUP BY reviewerID
            ORDER BY review_count DESC
            LIMIT 10
        ''', self.conn)
        
        print("Top 10 Most Active Reviewers:")
        for i, (_, row) in enumerate(top_reviewers.iterrows(), 1):
            days_active = (row['last_review'] - row['first_review']) / (60*60*24)
            print(f"   {i}. Reviewer {row['reviewerID'][:8]}...: {row['review_count']} reviews, "
                  f"{row['avg_rating']:.2f} avg, {days_active:.0f} days active")
        
        # Reviewer engagement distribution
        reviewer_stats = pd.read_sql_query('''
            SELECT 
                COUNT(*) as reviewer_count,
                AVG(review_count) as avg_reviews,
                MAX(review_count) as max_reviews
            FROM (
                SELECT reviewerID, COUNT(*) as review_count
                FROM reviews
                GROUP BY reviewerID
            )
        ''', self.conn)
        
        print(f"\nReviewer Engagement:")
        print(f"   Average reviews per reviewer: {reviewer_stats.iloc[0]['avg_reviews']:.1f}")
        print(f"   Most reviews by one reviewer: {reviewer_stats.iloc[0]['max_reviews']}")
        
        return top_reviewers, reviewer_stats
    
    def category_analysis(self):
        """Analyze differences between categories"""
        print("\n📚 CATEGORY ANALYSIS")
        print="="*60)
        
        category_stats = pd.read_sql_query('''
            SELECT 
                category,
                COUNT(*) as review_count,
                COUNT(DISTINCT asin) as product_count,
                COUNT(DISTINCT reviewerID) as reviewer_count,
                AVG(overall) as avg_rating,
                AVG(LENGTH(reviewText)) as avg_review_length
            FROM reviews
            GROUP BY category
            ORDER BY review_count DESC
        ''', self.conn)
        
        print("Category Performance:")
        for _, row in category_stats.iterrows():
            print(f"   {row['category'].title():<12}: {row['review_count']:>5,} reviews, "
                  f"{row['avg_rating']:.2f} avg, {row['avg_review_length']:.0f} chars")
        
        return category_stats
    
    def helpfulness_analysis(self):
        """Analyze review helpfulness"""
        print("\n👍 HELPFULNESS ANALYSIS")
        print="="*60)
        
        helpful_stats = pd.read_sql_query('''
            SELECT 
                CASE 
                    WHEN helpful > 0 THEN 'Helpful'
                    ELSE 'Not Helpful'
                END as helpfulness,
                COUNT(*) as review_count,
                AVG(overall) as avg_rating,
                AVG(LENGTH(reviewText)) as avg_length
            FROM reviews
            GROUP BY helpfulness
        ''', self.conn)
        
        print("Helpful vs Not Helpful Reviews:")
        for _, row in helpful_stats.iterrows():
            print(f"   {row['helpfulness']:<12}: {row['review_count']:>6,} reviews, "
                  f"{row['avg_rating']:.2f} avg rating, {row['avg_length']:.0f} chars")
        
        # Correlation between rating and helpfulness
        correlation = pd.read_sql_query('''
            SELECT 
                overall as rating,
                AVG(helpful) as avg_helpful_votes
            FROM reviews
            GROUP BY overall
            ORDER BY overall
        ''', self.conn)
        
        print(f"\nHelpfulness by Rating:")
        for _, row in correlation.iterrows():
            print(f"   {int(row['rating'])} stars: {row['avg_helpful_votes']:.2f} helpful votes on average")
        
        return helpful_stats, correlation
    
    def create_dashboard(self):
        """Create comprehensive visualization dashboard"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Amazon Product Reviews Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Rating Distribution
        rating_data = pd.read_sql_query('''
            SELECT overall, COUNT(*) as count
            FROM reviews
            GROUP BY overall
            ORDER BY overall
        ''', self.conn)
        
        axes[0,0].bar(rating_data['overall'], rating_data['count'], color='skyblue', alpha=0.7)
        axes[0,0].set_title('Rating Distribution', fontweight='bold')
        axes[0,0].set_xlabel('Star Rating')
        axes[0,0].set_ylabel('Number of Reviews')
        
        # 2. Reviews Over Time
        time_data = pd.read_sql_query('''
            SELECT 
                strftime('%Y-%m', datetime(unixReviewTime, 'unixepoch')) as month,
                COUNT(*) as review_count
            FROM reviews
            GROUP BY month
            ORDER BY month
        ''', self.conn)
        
        axes[0,1].plot(time_data['month'], time_data['review_count'], marker='o', linewidth=2)
        axes[0,1].set_title('Reviews Over Time', fontweight='bold')
        axes[0,1].set_xlabel('Month')
        axes[0,1].set_ylabel('Number of Reviews')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Category Distribution
        category_data = pd.read_sql_query('''
            SELECT category, COUNT(*) as review_count
            FROM reviews
            GROUP BY category
            ORDER BY review_count DESC
        ''', self.conn)
        
        axes[0,2].pie(category_data['review_count'], labels=category_data['category'], autopct='%1.1f%%')
        axes[0,2].set_title('Reviews by Category', fontweight='bold')
        
        # 4. Review Length Distribution
        length_data = pd.read_sql_query('''
            SELECT 
                CASE 
                    WHEN LENGTH(reviewText) < 50 THEN '0-50'
                    WHEN LENGTH(reviewText) < 200 THEN '50-200'
                    WHEN LENGTH(reviewText) < 500 THEN '200-500'
                    ELSE '500+'
                END as length_group,
                COUNT(*) as count,
                AVG(overall) as avg_rating
            FROM reviews
            WHERE reviewText IS NOT NULL
            GROUP BY length_group
        ''', self.conn)
        
        axes[1,0].bar(length_data['length_group'], length_data['count'], color='lightgreen')
        axes[1,0].set_title('Review Length Distribution', fontweight='bold')
        axes[1,0].set_xlabel('Review Length (chars)')
        axes[1,0].set_ylabel('Number of Reviews')
        
        # 5. Helpfulness vs Rating
        helpful_data = pd.read_sql_query('''
            SELECT overall, AVG(helpful) as avg_helpful
            FROM reviews
            GROUP BY overall
            ORDER BY overall
        ''', self.conn)
        
        axes[1,1].plot(helpful_data['overall'], helpful_data['avg_helpful'], marker='s', color='coral')
        axes[1,1].set_title('Helpfulness vs Rating', fontweight='bold')
        axes[1,1].set_xlabel('Star Rating')
        axes[1,1].set_ylabel('Average Helpful Votes')
        
        # 6. Reviewer Activity
        reviewer_data = pd.read_sql_query('''
            SELECT 
                CASE 
                    WHEN review_count = 1 THEN '1'
                    WHEN review_count <= 5 THEN '2-5'
                    WHEN review_count <= 10 THEN '6-10'
                    ELSE '10+'
                END as activity_level,
                COUNT(*) as reviewer_count
            FROM (
                SELECT reviewerID, COUNT(*) as review_count
                FROM reviews
                GROUP BY reviewerID
            )
            GROUP BY activity_level
        ''', self.conn)
        
        axes[1,2].pie(reviewer_data['reviewer_count'], labels=reviewer_data['activity_level'], autopct='%1.1f%%')
        axes[1,2].set_title('Reviewer Activity Levels', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('amazon_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*60)
        print("📊 AMAZON REVIEWS ANALYSIS REPORT")
        print("="*60)
        
        self.basic_overview()
        rating_dist, monthly_ratings = self.rating_analysis()
        top_products, product_stats = self.product_analysis()
        top_reviewers, reviewer_stats = self.reviewer_analysis()
        category_stats = self.category_analysis()
        helpful_stats, correlation = self.helpfulness_analysis()
        
        # Key Insights
        print("\n" + "="*60)
        print("💡 KEY INSIGHTS")
        print("="*60)
        
        # Rating insights
        five_star_pct = rating_dist[rating_dist['rating'] == 5]['percentage'].iloc[0]
        one_star_pct = rating_dist[rating_dist['rating'] == 1]['percentage'].iloc[0]
        print(f"• {five_star_pct}% of reviews are 5-star ratings")
        print(f"• Only {one_star_pct}% of reviews are 1-star ratings")
        
        # Product insights
        avg_reviews = product_stats.iloc[0]['avg_reviews_per_product']
        print(f"• Average of {avg_reviews:.1f} reviews per product")
        
        # Reviewer insights
        single_reviewers = reviewer_stats.iloc[0]['reviewer_count'] - len(top_reviewers)
        single_pct = (single_reviewers / reviewer_stats.iloc[0]['reviewer_count']) * 100
        print(f"• {single_pct:.1f}% of reviewers wrote only one review")
        
        # Category insights
        best_category = category_stats.iloc[0]['category']
        best_rating = category_stats[category_stats['avg_rating'] == category_stats['avg_rating'].max()].iloc[0]
        print(f"• {best_category} has the most reviews")
        print(f"• {best_rating['category']} has the highest average rating ({best_rating['avg_rating']:.2f})")
        
        self.create_dashboard()
        self.conn.close()

if __name__ == "__main__":
    eda = AmazonEDA()
    eda.generate_report()