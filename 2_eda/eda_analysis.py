"""
CodeAlpha Data Analytics Internship
TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
-----------------------------------------
Input: books_dataset.csv (produced by Task 1's web scraper)
Technique: pandas

What it does:
    - Loads the dataset and inspects structure (shape, dtypes, missing values)
    - Generates summary statistics
    - Explores trends: price by category, rating by category, correlations
    - Flags potential data issues (duplicates, outliers, missing values)
    - Prints a clean, readable EDA report to the console AND saves it to
      eda_report.txt

HOW TO USE ON YOUR OWN DATA:
    1. Change INPUT_FILE to your CSV path
    2. Update NUMERIC_COLUMNS / CATEGORY_COLUMNS to match your dataset's columns
"""

import pandas as pd

INPUT_FILE = "books_dataset.csv"
REPORT_FILE = "eda_report.txt"

NUMERIC_COLUMNS = ["price_gbp", "rating_stars"]
CATEGORY_COLUMNS = ["category"]

report_lines = []


def log(text=""):
    """Print to console AND collect for the saved report."""
    print(text)
    report_lines.append(str(text))


def section(title):
    log("\n" + "=" * 60)
    log(title)
    log("=" * 60)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # extract a numeric "available quantity" from strings like
    # "In stock (16 available)" - a common real-world cleaning step
    df["stock_qty"] = (
        df["availability"].str.extract(r"\((\d+) available\)").astype(float)
    )
    return df


def structure_overview(df: pd.DataFrame):
    section("1. DATASET STRUCTURE")
    log(f"Rows: {df.shape[0]}   Columns: {df.shape[1]}")
    log("\nColumn data types:")
    log(df.dtypes.to_string())
    log("\nFirst 5 rows:")
    log(df.head().to_string())


def missing_values_report(df: pd.DataFrame):
    section("2. MISSING VALUES")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_summary = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
    missing_summary = missing_summary[missing_summary["missing_count"] > 0]
    if missing_summary.empty:
        log("No missing values found.")
    else:
        log(missing_summary.to_string())


def duplicates_report(df: pd.DataFrame):
    section("3. DUPLICATE ROWS")
    dup_count = df.duplicated().sum()
    log(f"Fully duplicated rows: {dup_count}")
    title_dupes = df["title"].duplicated().sum()
    log(f"Duplicate titles (may be legitimate re-editions): {title_dupes}")


def summary_statistics(df: pd.DataFrame):
    section("4. SUMMARY STATISTICS (numeric columns)")
    log(df[NUMERIC_COLUMNS + ["stock_qty"]].describe().round(2).to_string())


def outlier_check(df: pd.DataFrame):
    section("5. OUTLIER CHECK (price, using IQR method)")
    q1 = df["price_gbp"].quantile(0.25)
    q3 = df["price_gbp"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df["price_gbp"] < lower) | (df["price_gbp"] > upper)]
    log(f"Price range considered normal: {lower:.2f} to {upper:.2f} GBP")
    log(f"Number of price outliers: {len(outliers)}")
    if not outliers.empty:
        log("\nSample outliers:")
        log(outliers[["title", "price_gbp", "category"]].head(10).to_string())


def category_trends(df: pd.DataFrame):
    section("6. TRENDS BY CATEGORY")
    trend = (
        df.groupby("category")
        .agg(
            book_count=("title", "count"),
            avg_price=("price_gbp", "mean"),
            avg_rating=("rating_stars", "mean"),
            total_stock=("stock_qty", "sum"),
        )
        .round(2)
        .sort_values("book_count", ascending=False)
    )
    log(trend.to_string())


def correlation_check(df: pd.DataFrame):
    section("7. CORRELATION BETWEEN NUMERIC FIELDS")
    corr = df[NUMERIC_COLUMNS + ["stock_qty"]].corr().round(3)
    log(corr.to_string())
    log(
        "\nInterpretation: values near +1 or -1 indicate a strong relationship; "
        "values near 0 indicate little to no linear relationship."
    )


def key_questions(df: pd.DataFrame):
    section("8. ANSWERING KEY QUESTIONS")
    most_expensive_cat = df.groupby("category")["price_gbp"].mean().idxmax()
    highest_rated_cat = df.groupby("category")["rating_stars"].mean().idxmax()
    cheapest_book = df.loc[df["price_gbp"].idxmin()]
    priciest_book = df.loc[df["price_gbp"].idxmax()]

    log(f"Category with highest average price: {most_expensive_cat}")
    log(f"Category with highest average rating: {highest_rated_cat}")
    log(f"Cheapest book: '{cheapest_book['title']}' at £{cheapest_book['price_gbp']}")
    log(f"Priciest book: '{priciest_book['title']}' at £{priciest_book['price_gbp']}")
    log(f"Overall average rating: {df['rating_stars'].mean():.2f} / 5")
    log(f"Percentage of books rated 4 stars or higher: "
        f"{(df['rating_stars'] >= 4).mean() * 100:.1f}%")


def save_report():
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n[Report saved to {REPORT_FILE}]")


if __name__ == "__main__":
    df = load_data(INPUT_FILE)
    structure_overview(df)
    missing_values_report(df)
    duplicates_report(df)
    summary_statistics(df)
    outlier_check(df)
    category_trends(df)
    correlation_check(df)
    key_questions(df)
    save_report()
