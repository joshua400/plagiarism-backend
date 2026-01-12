import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# --- Ensure required NLTK data is available (Render-safe) ---
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

try:
    sent_tokenize("Test sentence.")
except LookupError:
    nltk.download("punkt")

# Load stopwords
STOP_WORDS = set(stopwords.words("english"))


def preprocess(text: str) -> str:
    """
    Clean and normalize text:
    - lowercase
    - remove special characters
    - remove stopwords
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)

    tokens = text.split()
    tokens = [word for word in tokens if word not in STOP_WORDS]

    return " ".join(tokens)


def split_sentences(text: str):
    """
    Split text into sentences using NLTK
    """
    return sent_tokenize(text)
