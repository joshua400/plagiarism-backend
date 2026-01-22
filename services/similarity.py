from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts using TF-IDF."""
    if not text1 or not text2:
        return 0.0
    
    try:
        tfidf = TfidfVectorizer(stop_words='english').fit_transform([text1, text2])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(score)
    except:
        return 0.0

def classify_match(score):
    """Classify match type based on similarity score."""
    if score >= 0.75:
        return "exact"
    elif score >= 0.4:
        return "partial"
    return None
