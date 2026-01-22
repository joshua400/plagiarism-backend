import os
import requests

OPENSERP_URL = os.getenv("OPENSERP_URL")

def search_web(query):
    if not OPENSERP_URL:
        return []

    try:
        r = requests.get(
            OPENSERP_URL,
            params={"q": query, "engine": "duckduckgo"},
            timeout=8
        )
        return r.json().get("results", [])[:3]
    except:
        return []
