"""
British Airways customer review web scraper.

This script scrapes customer reviews for British Airways from the Skytrax Airline Quality website (https://www.airlinequality.com/).

Produces 3 CSV files:
- airline_reviews.csv
- seat_reviews.csv
- lounge_reviews.csv

Usage:
    $ python scrape_reviews.py

"""

import re
from typing import Dict, List
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
HEADERS = {"User-Agent": USER_AGENT}
BASE_URL_TEMPLATE = "https://www.airlinequality.com/{section}-reviews/british-airways/page/{page_num}/?sortby=post_date%3ADesc&pagesize=100"


def scrape_reviews(page_url: str) -> List[Dict[str, str]]:
    """
    Scrape reviews from given page URL.

    Args:
        page_url (str): URL of the page to scrape.

    Returns:
        List[Dict]: A list of dictionaries with review data.
    """
    try:
        response = requests.get(page_url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed for {page_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    reviews: List[Dict[str, str]] = []

    for review_block in soup.find_all("article", class_="list-item"):
        # Initialize the review dictionary
        review: Dict[str, str] = {}

        # Extract date
        review["Date"] = review_block.find("time").get("datetime", "N/A")

        # Extract rating
        rating = review_block.find("span", itemprop="ratingValue")
        if not rating:
            rating = review_block.find("div", class_="rating-10")
        review["Rating"] = rating.text.strip() if rating else "N/A"

        # Extract title
        title = review_block.find("h2", class_="text_header")
        review["Title"] = title.text.strip() if title else "N/A"

        # Extract author name
        author = review_block.find("span", itemprop="name")
        review["Author"] = author.text.strip() if author else "N/A"

        # Extract country
        user_info = review_block.find("h3", class_="userStatusWrapper")
        if user_info:
            user_info_text = user_info.text.strip()
            country_match = re.search(r"(?<=\().+?(?=\))", user_info_text)
            review["Country"] = country_match.group(0) if country_match else "N/A"
        else:
            review["Country"] = "N/A"

        # Extract review body
        review_body = review_block.find("div", itemprop="reviewBody")
        review["Review"] = review_body.text.strip() if review_body else "N/A"

        # Extract additional details and star ratings
        try:
            review_stats = review_block.find("table", class_="review-ratings").find_all("tr")
            for stat in review_stats:
                cells = stat.findChildren()
                label_text = cells[0].text.strip()
                value_text = cells[1].text.strip()

                # Check if the value is a star rating and count the number of filled stars
                if value_text == "12345":
                    value_text = str(len(cells[1].find_all("span", class_="star fill")))

                review[label_text] = value_text
            print(review)
        except AttributeError as e:
            print(f"Error parsing review stats: {e}")

        reviews.append(review)

    return reviews


def get_all_reviews(section: str, num_pages: int) -> List[Dict[str, str]]:
    """
    Get all reviews from specified number of pages.

    Args:
        section (str): The reviews section ("airline", "seat", or "lounge").
        num_pages (int): Number of pages to scrape.

    Returns:
        List[Dict]: A list of dictionaries containing review details.
    """
    all_reviews: List[Dict[str, str]] = []
    for page_num in range(1, num_pages + 1):
        page_url = BASE_URL_TEMPLATE.format(section=section, page_num=page_num)
        print(f"Scraping page {page_num} of {num_pages}...")
        all_reviews.extend(scrape_reviews(page_url))

    return all_reviews


def main() -> None:
    sections = ["airline", "seat", "lounge"]

    Path("data").mkdir(exist_ok=True)

    for section in sections:
        base_url = BASE_URL_TEMPLATE.format(section=section, page_num=1)

        try:
            response = requests.get(base_url, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve main page for {section}: {e}")
            continue
        # Parse the number of pages from the pagination section
        soup = BeautifulSoup(response.text, "html.parser")
        page_nav = soup.find("article", class_="comp_reviews-pagination")
        nav_items = page_nav.find_all("li")
        num_pages = int(nav_items[-2].get_text(strip=True))

        # Initiate the scraper
        reviews = get_all_reviews(section, num_pages)

        df = pd.DataFrame(reviews)
        df.to_csv(f"data/{section}_reviews.csv", index=False)

        print(f"Scraping {section} section completed and saved to {section}_reviews.csv")


if __name__ == "__main__":
    main()
