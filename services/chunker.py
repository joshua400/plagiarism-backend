def chunk_text(text, size=25, overlap=10):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = " ".join(words[i:i+size])
        if len(chunk.split()) >= 8:
            chunks.append(chunk)
    return chunks
