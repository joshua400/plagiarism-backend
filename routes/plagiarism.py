from fastapi import APIRouter
from services.chunker import chunk_text
from services.search import search_web
from services.extractor import extract_text
from services.similarity import similarity
from services.aggregator import classify

router = APIRouter()

@router.post("/check-plagiarism")
def check_plagiarism(data: dict):
    text = data.get("text", "")
    chunks = chunk_text(text)
    matches = []

    for chunk in chunks[:10]:
        results = search_web(chunk)

        for r in results:
            page_text = extract_text(r.get("link", ""))
            score = similarity(chunk, page_text)
            match_type = classify(score)

            if match_type:
                matches.append({
                    "sentence": chunk,
                    "source": r.get("link"),
                    "similarity": round(score, 2),
                    "type": match_type
                })

    plag = int((len(matches) / max(len(chunks), 1)) * 100)

    return {
        "plagiarism_percentage": plag,
        "unique_percentage": 100 - plag,
        "matches": matches
    }
