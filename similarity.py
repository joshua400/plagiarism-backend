from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def document_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(score)


def sentence_similarity(s1: str, s2: str) -> float:
    if not s1 or not s2:
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([s1, s2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(score)
