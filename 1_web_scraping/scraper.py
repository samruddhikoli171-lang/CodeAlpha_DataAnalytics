"""
CodeAlpha Data Analytics Internship
TASK 1: WEB SCRAPING
---------------------
Target: http://books.toscrape.com  (a site built for practicing scraping)
Technique: requests + BeautifulSoup

What it does:
    - Scrapes EVERY book across ALL category pages (1000 books, 50 pages)
    - Extracts: title, price, star rating, availability/stock, category
    - Saves a clean dataset to books_dataset.csv
      (this CSV is the input for Task 2 - EDA, and Task 3 - Visualization)

HOW TO ADAPT THIS TO A DIFFERENT SITE:
    1. Change BASE_URL
    2. Open the page in your browser -> right click an element -> Inspect
    3. Update the CSS selectors inside parse_book_list_page() / parse_book_detail()
"""

import csv
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
OUTPUT_FILE = "books_dataset.csv"
DELAY_SECONDS = 0.5  # be polite - don't hammer servers with requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}

# Star ratings on the site are written as CSS classes like "star-rating Three"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url: str):
    """Download a page and return a parsed BeautifulSoup object, or None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Failed to fetch {url}: {e}")
        return None


def parse_book_list_page(soup: BeautifulSoup, current_url: str) -> list[dict]:
    """Extract basic info + detail-page links for every book on a catalog page."""
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price_text = article.select_one(".price_color").get_text(strip=True)
        price = float(re.sub(r"[^\d.]", "", price_text))
        rating_class = article.select_one(".star-rating")["class"][1]  # e.g. "Three"
        rating = RATING_WORDS.get(rating_class, None)
        availability = article.select_one(".availability").get_text(strip=True)
        detail_url = requests.compat.urljoin(current_url, article.h3.a["href"])

        books.append({
            "title": title,
            "price_gbp": price,
            "rating_stars": rating,
            "availability": availability,
            "detail_url": detail_url,
        })
    return books


def get_category_from_detail_page(soup: BeautifulSoup) -> str:
    """Books.toscrape.com shows category in the breadcrumb trail."""
    breadcrumb = soup.select("ul.breadcrumb li a")
    if len(breadcrumb) >= 3:
        return breadcrumb[2].get_text(strip=True)
    return "Unknown"


def get_next_page_url(soup: BeautifulSoup, current_url: str):
    next_link = soup.select_one("li.next > a")
    if next_link:
        return requests.compat.urljoin(current_url, next_link["href"])
    return None


def scrape_all_books() -> list[dict]:
    all_books = []
    url = BASE_URL
    page_num = 1

    while url:
        print(f"Scraping catalog page {page_num}: {url}")
        soup = fetch_page(url)
        if soup is None:
            break

        page_books = parse_book_list_page(soup, url)
        all_books.extend(page_books)
        print(f"  -> found {len(page_books)} books (running total: {len(all_books)})")

        url = get_next_page_url(soup, url)
        page_num += 1
        time.sleep(DELAY_SECONDS)

    return all_books


def enrich_with_category(books: list[dict]) -> list[dict]:
    """Visit each book's detail page to grab its category (a second scraping pass)."""
    print(f"\nFetching category info for {len(books)} books (this takes a bit)...")
    for i, book in enumerate(books, start=1):
        soup = fetch_page(book["detail_url"])
        book["category"] = get_category_from_detail_page(soup) if soup else "Unknown"
        if i % 100 == 0:
            print(f"  -> processed {i}/{len(books)}")
        time.sleep(DELAY_SECONDS)
    return books


def save_to_csv(data: list[dict], filename: str):
    if not data:
        print("No data to save.")
        return
    # drop the internal-use detail_url column from the final dataset
    fieldnames = [k for k in data[0].keys() if k != "detail_url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({k: row[k] for k in fieldnames})
    print(f"\nSaved {len(data)} records to {filename}")


if __name__ == "__main__":
    books = scrape_all_books()
    books = enrich_with_category(books)
    save_to_csv(books, OUTPUT_FILE)
