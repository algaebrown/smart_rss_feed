import feedparser
from datetime import datetime
from typing import List
from newsletter import Newsletter
from dateutil import parser
import logging
import re
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def strip_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def clean_title(text: str) -> str:
    # Remove HTML tags and unwanted prefixes
    text = strip_html_tags(text)
    return text.replace("STAT+:", "").strip()


def get_publication_date_from_url(url: str) -> str:
    """
    Try to fetch the publication date from the article's webpage using common meta tags.
    Returns ISO date string if found, else None.
    """
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "lxml")
        # Try <meta property="article:published_time">
        meta = soup.find("meta", attrs={"property": "article:published_time"})
        if meta and meta.get("content"):
            return meta["content"]
        # Try <meta name="pubdate">
        meta = soup.find("meta", attrs={"name": "pubdate"})
        if meta and meta.get("content"):
            return meta["content"]
        # Try <meta name="date">
        meta = soup.find("meta", attrs={"name": "date"})
        if meta and meta.get("content"):
            return meta["content"]
    except Exception as e:
        logging.warning(f"Failed to fetch date from {url}: {e}")
    return None


def ingest_newsletters_from_feed(feed_path: str) -> List[Newsletter]:
    logging.info(f"Parsing feed: {feed_path}")
    feed = feedparser.parse(feed_path)
    logging.info(f"Feed title: {feed.feed.get('title', 'N/A')}")
    logging.info(f"Feed link: {feed.feed.get('link', 'N/A')}")
    newsletters = []
    for i, entry in enumerate(feed.entries):
        logging.info(f"Processing entry {i+1}/{len(feed.entries)}")
        raw_title = entry.get("title", "")
        title = clean_title(raw_title)
        content = entry.get("summary", "")  # 'summary' or 'description'
        publication_date = parser.parse(entry.get("published", ""))
        url = entry.get("link", "")
        # parse domain name from url if possible
        domain = re.findall(r"https?://([^/]+)/?", url)
        # Try to get date from the web page if possible
        # web_date = get_publication_date_from_url(url) if url else None
        # try:
        #     publication_date = (
        #         parser.parse(web_date)
        #         if web_date
        #         else (parser.parse(date_str) if date_str else datetime.now())
        #     )
        # except Exception as e:
        #     logging.warning(f"Failed to parse date for entry '{title}': {e}")
        #     publication_date = datetime.now()
        newsletters.append(
            Newsletter(
                title=title,
                content=content,
                publication_date=publication_date,
                url=url,
                domain=domain[0] if domain else None,
            )
        )
        logging.info(f"Added newsletter: {title} | {publication_date}")
    logging.info(f"Total newsletters ingested: {len(newsletters)}")
    return newsletters


def demo_ingest():
    logging.info("Starting demo ingestion...")
    newsletters = ingest_newsletters_from_feed("data/master_feed.xml")
    for n in newsletters:
        print(f"Title: {n.title}")
        print(f"Content: {n.content}")
        print(f"Publication Date: {n.publication_date}")
        print(f"URL: {n.url}")
        print("-" * 40)
    logging.info("Demo ingestion complete.")


if __name__ == "__main__":
    demo_ingest()
