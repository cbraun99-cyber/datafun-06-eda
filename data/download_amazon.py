import requests
import os
import pandas as pd
from io import StringIO
import gzip
import json

def download_amazon_data():
    """Download Amazon product review data"""
    
    os.makedirs('data', exist_ok=True)
    
    # Amazon product data sources (smaller subsets for demo)
    datasets = {
        'electronics': 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz',
        'books': 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Books_5.json.gz',
        'movies_tv': 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Movies_and_TV_5.json.gz'
    }
    
    print("📥 Downloading Amazon Review Datasets...")
    
    for category, url in datasets.items():
        try:
            print(f"Downloading {category} reviews...")
            
            # Download and extract
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Save compressed file
            gz_path = f'data/reviews_{category}.json.gz'
            with open(gz_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract and convert to CSV
            extract_amazon_reviews(gz_path, category)
            print(f"✅ {category} data processed")
            
        except Exception as e:
            print(f"❌ Error downloading {category}: {e}")

def extract_amazon_reviews(gz_path, category):
    """Extract and process Amazon review data"""
    
    reviews = []
    with gzip.open(gz_path, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10000:  # Limit to 10k reviews per category for demo
                break
            if line.strip():
                try:
                    review = json.loads(line)
                    reviews.append({
                        'reviewerID': review.get('reviewerID', ''),
                        'asin': review.get('asin', ''),  # Product ID
                        'reviewerName': review.get('reviewerName', ''),
                        'helpful': review.get('helpful', [0, 0])[0],  # Helpful votes
                        'reviewText': review.get('reviewText', ''),
                        'overall': review.get('overall', 0),
                        'summary': review.get('summary', ''),
                        'unixReviewTime': review.get('unixReviewTime', 0),
                        'reviewTime': review.get('reviewTime', '')
                    })
                except json.JSONDecodeError:
                    continue
    
    # Create DataFrame and save
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_csv(f'data/amazon_reviews_{category}.csv', index=False)
        print(f"   Saved {len(df)} {category} reviews")

def download_metadata():
    """Download product metadata"""
    print("\n📋 Downloading product metadata...")
    
    # Product metadata (small subset)
    metadata_urls = {
        'electronics': 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz',
        'books': 'http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Books.json.gz'
    }
    
    for category, url in metadata_urls.items():
        try:
            print(f"Downloading {category} metadata...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            gz_path = f'data/metadata_{category}.json.gz'
            with open(gz_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            extract_metadata(gz_path, category)
            
        except Exception as e:
            print(f"❌ Error downloading {category} metadata: {e}")

def extract_metadata(gz_path, category):
    """Extract product metadata"""
    
    products = []
    with gzip.open(gz_path, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5000:  # Limit for demo
                break
            if line.strip():
                try:
                    product = json.loads(line)
                    products.append({
                        'asin': product.get('asin', ''),
                        'title': product.get('title', ''),
                        'price': product.get('price', 0),
                        'brand': product.get('brand', ''),
                        'categories': str(product.get('categories', [])),
                        'description': str(product.get('description', '')),
                        'also_bought': str(product.get('also_bought', [])),
                        'salesRank': str(product.get('salesRank', {}))
                    })
                except:
                    continue
    
    if products:
        df = pd.DataFrame(products)
        df.to_csv(f'data/amazon_products_{category}.csv', index=False)
        print(f"   Saved {len(df)} {category} products")

def manual_download_instructions():
    """Instructions for full dataset download"""
    print("\n" + "="*60)
    print("📚 FULL DATASET DOWNLOAD INSTRUCTIONS")
    print("="*60)
    print("For the complete Amazon dataset (recommended):")
    print("1. Visit: https://nijianmo.github.io/amazon/index.html")
    print("2. Download files for your desired categories:")
    print("   - reviews_*.json.gz (review data)")
    print("   - meta_*.json.gz (product metadata)")
    print("3. Place files in the 'data' folder")
    print("4. Run: python scripts/process_full_dataset.py")

if __name__ == "__main__":
    download_amazon_data()
    download_metadata()
    manual_download_instructions()