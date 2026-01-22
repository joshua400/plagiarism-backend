from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity(a, b):
    tfidf = TfidfVectorizer().fit_transform([a, b])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
