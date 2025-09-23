# datafun-06-eda
# Module 6 Repository - EDA
### Author: Chris Braun

## 🚀 Quick Start

```bash
# Create virtual environment
py -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
py -m pip install -r requirements.txt

# Download Amazon dataset
py data/download_amazon.py

# Initialize database
py scripts/init_database.py

# Run EDA analysis
py scripts/amazon_eda.py

# Or run the complete analysis
py run_amazon_analysis.py
```

## Remember to occasionally run
1. ```git add .```
2. ```git commit -m "Comment"```
3. ```git push - u origin main``` or ```git push```

## 📊 Project Overview
This project performs comprehensive Exploratory Data Analysis (EDA) on Amazon product review data. The analysis includes rating patterns, customer behavior, product performance, sentiment analysis, and temporal trends using real Amazon review data.

## 🛍️ Dataset Information
**Amazon Product Reviews Dataset-** Contains real Amazon customer reviews across multiple categories:

*Electronics

*Books

*Movies & TV

*And more...

**Dataset Features:**

*Product ratings (1-5 stars)

*Review text and summaries

*Reviewer information

*Helpfulness votes

*Timestamps

*Product categories

## 📁 Project Structure

```text
amazon-eda/
├── data/
│   ├── download_amazon.py
│   └── (dataset files)
├── scripts/
│   ├── init_database.py
│   ├── amazon_eda.py
│   ├── product_analysis.py
│   ├── review_analysis.py
│   ├── sentiment_analysis.py
│   └── category_analysis.py
├── requirements.txt
└── README.md
```

## 🔧 Installation & Setup
Prerequisites
*Python 3.7+

*pip package manager

*Internet connection (for data download)

### Step-by-Step Setup
1. Clone the repository

```bash
git clone <your-repo-url>
cd datafun-06-eda
```
2. Set up virtual environment

```bash
py -m venv .venv
.venv\Scripts\activate
```
3. Install dependencies

```bash
py -m pip install -r requirements.txt
```
4. Download the data

```bash
py data/download_amazon.py
```
5. Initialize the database

```bash
py scripts/init_database.py
```

## 📈 Analysis Features
### Core EDA Analyses
* **Rating Distribution:** Analysis of star rating patterns

* **Temporal Trends:** Review activity over time

* **Product Popularity:** Most reviewed products and categories

* **Reviewer Behavior:** Customer engagement patterns

* **Category Analysis:** Performance across product categories

* **Helpfulness Metrics:** What makes reviews helpful

## Advanced Analyses
* Sentiment Analysis: NLP-based sentiment scoring of review text

* Correlation Analysis: Relationships between rating, helpfulness, and review length

* Geographic Trends: Regional patterns (if location data available)

##Visualization Outputs
The analysis generates comprehensive visualizations including:

* Rating distribution charts

* Monthly review trends

* Category performance pie charts

* Reviewer activity levels

* Sentiment vs rating correlations