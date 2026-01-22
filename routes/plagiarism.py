from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor
from services.chunker import split_sentences, chunk_text
from services.search import search_web
from services.extractor import extract_text
from services.similarity import calculate_similarity, classify_match
from services.aggregator import calculate_percentages

router = APIRouter()

class TextInput(BaseModel):
    text: str

def process_url(url, title, snippet):
    """Worker function for parallel extraction."""
    page_text = extract_text(url)
    if not page_text:
        page_text = snippet
    return {"url": url, "title": title, "content": page_text}

@router.post("/check-plagiarism")
def check_plagiarism(data: TextInput):
    text = data.text.strip()
    
    if not text:
        return {
            "wordCount": 0,
            "characterCount": 0,
            "plagiarismPercentage": 0,
            "exactMatchPercentage": 0,
            "partialMatchPercentage": 0,
            "uniquePercentage": 100,
            "highlightedText": [],
            "sources": []
        }
    
    # Count words and characters
    word_count = len(text.split())
    char_count = len(text)
    
    # Split into sentences for highlighting
    sentences = split_sentences(text)
    
    # Create search chunks
    chunks = chunk_text(text)
    
    # Step 1: Collect unique URLs from search results
    unique_urls = {} # url -> {title, snippet}
    for chunk in chunks[:8]: # Limit chunks to speed up search
        results = search_web(chunk)
        for result in results:
            url = result.get("link", "")
            if url and url not in unique_urls:
                unique_urls[url] = {
                    "title": result.get("title", "Untitled"),
                    "snippet": result.get("snippet", "")
                }
            if len(unique_urls) >= 12: # Limit total sources to process
                break
        if len(unique_urls) >= 12:
            break

    # Step 2: Parallel content extraction
    extracted_contents = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_url, url, info["title"], info["snippet"])
            for url, info in unique_urls.items()
        ]
        for future in futures:
            try:
                extracted_contents.append(future.result(timeout=10))
            except Exception as e:
                print(f"Parallel extraction error: {e}")

    # Step 3: Compare sentences with extracted contents
    sources = []
    source_map = {} # url -> source index
    sentence_matches = {} # sentence -> (match_type, source_index, score)

    for item in extracted_contents:
        url = item["url"]
        title = item["title"]
        page_text = item["content"]
        
        if not page_text:
            continue

        for sentence in sentences:
            if sentence in sentence_matches and sentence_matches[sentence][2] > 0.95:
                continue # Skip if already found an exact match
            
            score = calculate_similarity(sentence, page_text)
            match_type = classify_match(score)
            
            if match_type:
                # Better match or first match
                if sentence not in sentence_matches or score > sentence_matches[sentence][2]:
                    if url not in source_map:
                        source_index = len(sources)
                        source_map[url] = source_index
                        sources.append({
                            "title": title,
                            "url": url,
                            "matchedText": sentence[:100] + "..." if len(sentence) > 100 else sentence
                        })
                    else:
                        source_index = source_map[url]
                    
                    sentence_matches[sentence] = (match_type, source_index, score)
    
    # Build highlighted text array
    highlighted_text = []
    for sentence in sentences:
        if sentence in sentence_matches:
            match_type, source_index, score = sentence_matches[sentence]
            highlighted_text.append({
                "text": sentence,
                "type": match_type,
                "sourceIndex": source_index,
                "similarity": round(score, 2)
            })
        else:
            highlighted_text.append({
                "text": sentence,
                "type": "unique",
                "sourceIndex": None,
                "similarity": 0
            })
    
    # Calculate percentages
    percentages = calculate_percentages(highlighted_text, len(sentences))
    
    return {
        "wordCount": word_count,
        "characterCount": char_count,
        **percentages,
        "highlightedText": highlighted_text,
        "sources": sources
    }
