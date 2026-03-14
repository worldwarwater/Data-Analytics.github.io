# Fiction Book Web Scraper

## Overview
An automated web scraper that extracts fiction book data (title, price, availability, and rating) from an online bookstore. The scraper navigates across multiple pages, collects structured data, and exports it to CSV format for further analysis.

## Features
- Scrapes all fiction books across multiple paginated pages automatically
- Extracts title, price, availability status, and star rating for each book
- Converts ratings from text (e.g., "Three") to numeric values (1-5)
- Includes polite rate limiting (1-second delay between requests)
- Exports clean, analysis-ready data to CSV with computed numeric price column
- Prints summary statistics (average price, price range, average rating)

## Files
| File | Description |
|------|-------------|
| `book_scraper.py` | Main scraper script |
| `fiction_books.csv` | Output dataset with scraped book data |
| `requirements.txt` | Python dependencies |

## How to Run
```bash
pip install -r requirements.txt
python book_scraper.py
```

## Sample Output
```
Scraping page 1...
  Found 20 books (total: 20)
Scraping page 2...
  Found 5 books (total: 25)

Saved 25 books to fiction_books.csv
Average price: £31.45
Price range: £10.79 - £53.74
Average rating: 3.2/5
```

## Tools & Libraries
- Python 3
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP requests)
- Pandas (data manipulation and CSV export)

## Author
**Stephen Drani** — [LinkedIn](https://linkedin.com/in/stephen-drani-a58140232) | [GitHub](https://github.com/worldwarwater)
