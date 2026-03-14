"""
Book Web Scraper
Author: Stephen Drani
Description: Scrapes fiction book data (title, price, availability, rating)
             from an online bookstore across multiple pages.
             Outputs structured data to CSV for analysis.
Tools: Python, BeautifulSoup, Requests, Pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://books.toscrape.com/catalogue/category/books/fiction_10/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_page(url):
    """Fetch a page and return BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_books(soup):
    """Extract book data from a single page."""
    books = []
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text.strip()
        availability = article.find("p", class_="instock availability").text.strip()
        rating_class = article.find("p", class_="star-rating")["class"][1]
        rating = RATING_MAP.get(rating_class, 0)
        link = article.h3.a["href"]

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "detail_url": link
        })

    return books


def get_next_page(soup, current_url):
    """Check if there's a next page and return its URL."""
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_href = next_btn.a["href"]
        base = current_url.rsplit("/", 1)[0]
        return f"{base}/{next_href}"
    return None


def scrape_all_books():
    """Scrape all pages of fiction books."""
    all_books = []
    url = BASE_URL
    page_num = 1

    while url:
        print(f"Scraping page {page_num}... ({url})")
        soup = get_page(url)
        books = parse_books(soup)
        all_books.extend(books)
        print(f"  Found {len(books)} books (total: {len(all_books)})")

        url = get_next_page(soup, url)
        page_num += 1
        time.sleep(1)  # Polite delay between requests

    return all_books


def save_to_csv(books, filename="fiction_books.csv"):
    """Save book data to CSV file."""
    df = pd.DataFrame(books)
    df["price_numeric"] = df["price"].str.replace("£", "").astype(float)
    df = df.sort_values("price_numeric", ascending=False)

    output_path = os.path.join(os.path.dirname(__file__), filename)
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} books to {output_path}")
    print(f"Average price: £{df['price_numeric'].mean():.2f}")
    print(f"Price range: £{df['price_numeric'].min():.2f} - £{df['price_numeric'].max():.2f}")
    print(f"Average rating: {df['rating'].mean():.1f}/5")

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("Fiction Book Web Scraper")
    print("=" * 60)

    books = scrape_all_books()
    df = save_to_csv(books)

    print("\nTop 5 most expensive fiction books:")
    print(df[["title", "price", "rating"]].head().to_string(index=False))
