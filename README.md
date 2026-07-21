# CodeAlpha Data Analytics Internship – Submission

This repo covers **3 of the 4 tasks** (Web Scraping, EDA, Data Visualization),
built as one connected pipeline: scrape → analyze → visualize.

## Projects

### 1. `1_web_scraping/` – Task 1: Web Scraping
Scrapes all 1000 books from books.toscrape.com (title, price, rating,
availability, category) using `requests` + `BeautifulSoup`. Outputs
`books_dataset.csv`.

```
cd 1_web_scraping
pip install -r requirements.txt
python scraper.py
```
Takes ~10-12 minutes (visits every book's detail page for category data).
A ready-made `sample_books_dataset.csv` (1000 rows, same schema) is included
one level up if you want to test Tasks 2 & 3 immediately without waiting.

### 2. `2_eda/` – Task 2: Exploratory Data Analysis
Loads the scraped CSV with `pandas` and produces: structure overview,
missing-value check, duplicate check, summary statistics, outlier detection,
category-level trends, correlations, and answers to key questions. Saves
`eda_report.txt`.

```
cd 2_eda
pip install -r requirements.txt
# copy the dataset in first:
cp ../sample_books_dataset.csv books_dataset.csv    # or your own scraped CSV
python eda_analysis.py
```

### 3. `3_data_visualization/` – Task 3: Data Visualization
Loads the same dataset and generates 6 charts (price distribution, books per
category, average price per category, rating distribution, average rating
per category, price vs. rating) plus a combined `dashboard.png`.

```
cd 3_data_visualization
pip install -r requirements.txt
cp ../sample_books_dataset.csv books_dataset.csv    # or your own scraped CSV
python visualize.py
```

## For your submission checklist
- [ ] Rename this repo to `CodeAlpha_DataAnalytics` (or similar) when you push to GitHub
- [ ] Run the real scraper (Task 1) to get your own live `books_dataset.csv`
- [ ] Re-run Tasks 2 & 3 on that real data so your report/charts reflect it
- [ ] Record a short video walking through the code + results, post on LinkedIn
      tagging @CodeAlpha with your GitHub link
- [ ] Submit via the WhatsApp-group submission form
