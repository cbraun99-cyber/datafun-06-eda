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

### Advanced Analyses
* Sentiment Analysis: NLP-based sentiment scoring of review text

* Correlation Analysis: Relationships between rating, helpfulness, and review length

* Geographic Trends: Regional patterns (if location data available)

###
 Visualization Outputs
The analysis generates comprehensive visualizations including:

* Rating distribution charts

* Monthly review trends

* Category performance pie charts

* Reviewer activity levels

* Sentiment vs rating correlations

## 🎯 Key Business Questions Answered
1. **Customer Behavior**

  * What percentage of reviews are 5-star vs 1-star?

  * How do review patterns vary by product category?

  * What's the average rating across different product types?

2. **Product Performance**

  * Which products receive the most reviews?

  * Is there correlation between review quantity and rating?

  * How do product categories compare in customer satisfaction?

3. **Temporal Analysis**

  * How has review volume changed over time?

  * Are there seasonal patterns in review activity?

  * How do ratings trend over different time periods?
  
## 🐍 Python Scripts Overview
#### ```run_amazon_analysis.py``` 

Main execution script that runs the complete analysis pipeline.

#### ```scripts/amazon_eda.py```

Comprehensive EDA class with methods for:

* Basic dataset statistics

* Rating distribution analysis

* Product and reviewer behavior

* Category comparisons

* Visualization generation

#### ```scripts/sentiment_analysis.py```

Advanced NLP analysis using TextBlob for:

* Sentiment polarity scoring

* Sentiment vs rating correlations

* Text-based insights

#### ```scripts/init_database.py```

Database management including:

* SQLite database creation

* Data loading from CSV files

* Index creation for performance

* Data quality checks

## 📊 Expected Outputs
Running the analysis will generate:

1. Console Reports with key statistics and insights

2. Visualization Files:

  * **amazon_analysis_dashboard.png** - Comprehensive dashboard

  * **sentiment_vs_rating.png** - Sentiment correlation analysis

3. SQLite Database:

  * **amazon_reviews.db** - Structured data for further analysis

## 🔍 Sample Insights You'll Discover
* Distribution of star ratings across products

* Most active reviewers and their rating patterns

* Category-wise performance differences

* Relationship between review length and helpfulness

* Temporal trends in customer feedback

* Sentiment analysis correlations with star ratings

## 🛠️ Technical Stack
* **Python 3.7+** - Core programming language

* **pandas** - Data manipulation and analysis

* **matplotlib/seaborn** - Data visualization

* **SQLite** - Database storage

* **TextBlob** - NLP sentiment analysis

* **requests** - HTTP data downloading

## 🚨 Troubleshooting
### Common Issues
### Dataset download fails:

```bash
# Manual download option:
# Visit: https://nijianmo.github.io/amazon/index.html
# Download files and place in data/ folder
```
### SQLite database errors:

```bash
# Reinitialize database:
py scripts/init_database.py
```
### Missing dependencies:

```bash
# Reinstall requirements:
py -m pip install -r requirements.txt

# For TextBlob NLP features:
python -m textblob.download_corpora
```
### Memory issues with large datasets:

* Reduce sample size in download scripts

* Use category-specific analysis instead of full dataset

## 📚 Learning Outcomes
This project demonstrates:

* Real-world EDA on large-scale e-commerce data

* SQL database management with Python

* Advanced data visualization techniques

* NLP sentiment analysis application

* Business intelligence insights generation

* Professional reporting and documentation

## 🔄 Project Maintenance
#### Regular Updates
* Monitor dataset source for updates

* Refresh analysis with new data periodically

* Update visualizations and insights

## Extending the Analysis
Potential enhancements include:

* Integration with additional data sources

* Machine learning predictions

* Real-time analysis capabilities

* Web dashboard development

## 📞 Support
For issues or questions:

1. Check the troubleshooting section above

2. Review script documentation strings

3. Examine generated error logs

4. Consult Python package documentation

## Special Note

Using the .gitignore in this file will ignore the .gz files that are downloaded. They don't need to be added to the repository, as they are downloaded when you run the scripts.
