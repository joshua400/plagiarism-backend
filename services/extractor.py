import requests
from bs4 import BeautifulSoup

def extract_text(url):
    """Fetch and extract text from a URL with a browser-like User-Agent."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=6)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        return soup.get_text(" ", strip=True)
    except Exception as e:
        print(f"Extraction error for {url}: {e}")
        return ""
