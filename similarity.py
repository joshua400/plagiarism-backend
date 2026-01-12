from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def document_similarity(doc1: str, doc2: str) -> float:
    if not doc1.strip() or not doc2.strip():
        return 0.0

    vectorizer = TfidfVectorizer(ngram_range=(1, 3))
    tfidf = vectorizer.fit_transform([doc1, doc2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])

    return float(score[0][0])

def sentence_similarity(sent1: str, sent2: str) -> float:
    if not sent1.strip() or not sent2.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([sent1, sent2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])

    return float(score[0][0])
