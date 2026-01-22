from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.chunker import split_sentences, chunk_text
from services.search import search_web
from services.extractor import extract_text
from services.similarity import calculate_similarity, classify_match
from services.aggregator import calculate_percentages

router = APIRouter()

class TextInput(BaseModel):
    text: str

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
    
    # Create search chunks (larger chunks for better search results)
    chunks = chunk_text(text)
    
    # Track sources and matches
    sources = []
    source_map = {}  # url -> source index
    sentence_matches = {}  # sentence -> (match_type, source_index, score)
    
    # Search for each chunk
    for chunk in chunks[:12]:  # Increased from 8 to catch more sources
        results = search_web(chunk)
        
        for result in results:
            url = result.get("link", "")
            title = result.get("title", "Untitled")
            snippet = result.get("snippet", "")
            
            if not url:
                continue
            
            # Extract page content
            page_text = extract_text(url)
            if not page_text:
                page_text = snippet  # Fallback to snippet
            
            # Check each sentence against this source
            for sentence in sentences:
                if sentence in sentence_matches:
                    continue  # Already found a match for this sentence
                
                # Calculate similarity
                score = calculate_similarity(sentence, page_text)
                match_type = classify_match(score)
                
                if match_type:
                    # Add source if not already added
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
