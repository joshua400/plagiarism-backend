from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts using TF-IDF with N-grams."""
    if not text1 or not text2:
        return 0.0
    
    try:
        # Using analyzer='char_wb' or ngram_range can help with paraphrasing
        tfidf = TfidfVectorizer(
            stop_words='english', 
            ngram_range=(1, 2)  # Capture pairs of words to detect structure
        ).fit_transform([text1, text2])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(score)
    except:
        return 0.0

def classify_match(score):
    """Classify match type based on similarity score."""
    if score >= 0.70:
        return "exact"
    elif score >= 0.25:  # Lowered from 0.4 to catch more paraphrasing
        return "partial"
    return None
