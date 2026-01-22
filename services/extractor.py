import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        html = requests.get(url, timeout=6).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(" ")
    except:
        return ""
