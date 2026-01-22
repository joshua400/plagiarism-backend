from ddgs import DDGS

def search_web(query):
    """Search the web using DuckDuckGo (free, no API key needed)."""
    try:
        results = list(DDGS().text(query, max_results=5))
        return [
            {
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", "")
            }
            for r in results
        ]
    except Exception as e:
        print(f"Search error: {e}")
        return []
