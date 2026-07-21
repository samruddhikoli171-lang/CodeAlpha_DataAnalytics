"""
CodeAlpha Data Analytics Internship
TASK 3: DATA VISUALIZATION
-----------------------------
Input: books_dataset.csv (produced by Task 1's web scraper)
Technique: matplotlib + seaborn

What it does:
    - Loads the dataset
    - Generates 6 charts that turn the raw data into visual insights:
        1. Price distribution (histogram)
        2. Number of books per category (bar chart)
        3. Average price per category (bar chart)
        4. Rating distribution (bar chart)
        5. Average rating per category (bar chart)
        6. Price vs rating relationship (scatter plot)
    - Saves each chart as a PNG AND combines them into one dashboard image
      (dashboard.png) - great for a portfolio/LinkedIn post

HOW TO USE ON YOUR OWN DATA:
    1. Change INPUT_FILE
    2. Update column names in each chart function to match your dataset
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # render to file, no GUI needed
import matplotlib.pyplot as plt
import seaborn as sns

INPUT_FILE = "books_dataset.csv"
OUTPUT_DIR = "."

sns.set_theme(style="whitegrid")
PALETTE = "viridis"


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def chart_price_distribution(df, ax):
    sns.histplot(df["price_gbp"], bins=25, kde=True, color="#4C72B0", ax=ax)
    ax.set_title("Price Distribution")
    ax.set_xlabel("Price (GBP)")
    ax.set_ylabel("Number of Books")


def chart_books_per_category(df, ax):
    counts = df["category"].value_counts().sort_values(ascending=False)
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Books per Category")
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("")


def chart_avg_price_per_category(df, ax):
    avg_price = df.groupby("category")["price_gbp"].mean().sort_values(ascending=False)
    sns.barplot(x=avg_price.values, y=avg_price.index, hue=avg_price.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Average Price per Category")
    ax.set_xlabel("Average Price (GBP)")
    ax.set_ylabel("")


def chart_rating_distribution(df, ax):
    counts = df["rating_stars"].value_counts().sort_index()
    sns.barplot(x=counts.index, y=counts.values, hue=counts.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Rating Distribution")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Number of Books")


def chart_avg_rating_per_category(df, ax):
    avg_rating = df.groupby("category")["rating_stars"].mean().sort_values(ascending=False)
    sns.barplot(x=avg_rating.values, y=avg_rating.index, hue=avg_rating.index,
                palette=PALETTE, legend=False, ax=ax)
    ax.set_title("Average Rating per Category")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("")


def chart_price_vs_rating(df, ax):
    sns.scatterplot(data=df, x="rating_stars", y="price_gbp",
                     hue="category", palette=PALETTE, alpha=0.6, legend=False, ax=ax)
    ax.set_title("Price vs Rating")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Price (GBP)")


def build_dashboard(df):
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))
    fig.suptitle("Book Catalog Analysis Dashboard", fontsize=18, fontweight="bold")

    chart_price_distribution(df, axes[0, 0])
    chart_books_per_category(df, axes[0, 1])
    chart_avg_price_per_category(df, axes[0, 2])
    chart_rating_distribution(df, axes[1, 0])
    chart_avg_rating_per_category(df, axes[1, 1])
    chart_price_vs_rating(df, axes[1, 2])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{OUTPUT_DIR}/dashboard.png", dpi=150)
    plt.close()
    print("Saved combined dashboard.png")


def save_individual_charts(df):
    chart_functions = {
        "price_distribution.png": chart_price_distribution,
        "books_per_category.png": chart_books_per_category,
        "avg_price_per_category.png": chart_avg_price_per_category,
        "rating_distribution.png": chart_rating_distribution,
        "avg_rating_per_category.png": chart_avg_rating_per_category,
        "price_vs_rating.png": chart_price_vs_rating,
    }
    for filename, func in chart_functions.items():
        fig, ax = plt.subplots(figsize=(9, 6))
        func(df, ax)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/{filename}", dpi=150)
        plt.close()
        print(f"Saved {filename}")


if __name__ == "__main__":
    df = load_data(INPUT_FILE)
    save_individual_charts(df)
    build_dashboard(df)
    print("\nAll charts generated successfully.")
