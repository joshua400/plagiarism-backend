import re

def split_sentences(text):
    """Split text into sentences for analysis."""
    # Split on common sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Filter out empty sentences
    return [s.strip() for s in sentences if s.strip() and len(s.split()) >= 3]

def chunk_text(text, size=20, overlap=8):
    """Chunk text into overlapping segments for search queries."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = " ".join(words[i:i+size])
        if len(chunk.split()) >= 5:  # Lowered from 8 to catch hits in shorter paragraphs
            chunks.append(chunk)
    return chunks
