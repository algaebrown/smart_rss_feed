def fetch_article_full_text(url: str) -> str:
    """
    Fetch the main article text from a URL using newspaper3k.
    Returns the article text, or an error message if fetching/parsing fails.
    Tolerates network errors, 403 forbidden, and parsing exceptions.
    """
    
    from newspaper import Article
    
    article = Article(url)
    article.download()
    article.parse()
    return article.text.strip() if article.text else "No article text found."

def duckduckgo_search_similar_news(query: str, max_results: int = 10) -> list:
    """
    Search DuckDuckGo for similar news or the original press release.
    Returns a list of dicts with 'title', 'url', and 'snippet'.
    Requires: pip install duckduckgo-search
    """
    
    from ddgs import DDGS
    results = []

    search_term = f'{query} news press release'
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(search_term, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        results.append({"title": "DuckDuckGo search error", "url": "", "snippet": str(e)})

    # filter for PR newswire
    for r in results:
        if 'www.prnewswire.com' in r['url']:
            full_text = fetch_article_full_text(r['url'])
            return full_text
    
    # if no PR newswire, try to scrape 3 other news articles
    success = 0
    full_text = ""
    for r in results:
        if success >= 3:
            break
        try:
            full_text += fetch_article_full_text(r['url'])
            success += 1
        except Exception:
            pass
    

    return full_text

def find_full_text(url, title):
    """
    Try to fetch the full article text from the given URL.
    If forbidden or error, search DuckDuckGo for similar news articles.
    Returns the article text or a message if not found.
    """
    try:
        article_text = fetch_article_full_text(url)
        if "forbidden" in article_text.lower() or "error" in article_text.lower():
            raise Exception("Access forbidden or error fetching article.")
        return article_text
    except Exception as e:
        print(f"Error fetching article from URL: {e}")
        print("Searching DuckDuckGo for similar news...")
        search_results = duckduckgo_search_similar_news(title)
        if search_results:
            return search_results
        else:
            return "No similar articles found."

if __name__ == "__main__":
    # Example URL (may trigger 403 or work depending on site)
    url = "https://www.fiercebiotech.com/cro/korean-cro-corestemchemon-inks-collaboration-expand-organoids-and-transcriptomics"

    title = "Korean CRO Corestem/Chemon inks collaboration to expand organoids and transcriptomics services"
    article_text = find_full_text(url, title)
    print(article_text)