from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from preprocess import preprocess, split_sentences
from similarity import document_similarity, sentence_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-plagiarism")
async def check_plagiarism(
    document1: UploadFile = File(...),
    document2: UploadFile = File(...),
):
    try:
        text1 = (await document1.read()).decode("utf-8", errors="ignore").strip()
        text2 = (await document2.read()).decode("utf-8", errors="ignore").strip()

        if not text1 or not text2:
            raise HTTPException(status_code=400, detail="Uploaded files are empty")

        clean1 = preprocess(text1)
        clean2 = preprocess(text2)

        if not clean1 or not clean2:
            return {
                "similarity_score": 0.0,
                "plagiarism_level": "Low",
                "plagiarized_sentences": []
            }

        doc_score = document_similarity(clean1, clean2)

        level = (
            "High" if doc_score >= 0.85 else
            "Moderate" if doc_score >= 0.6 else
            "Low"
        )

        plagiarized = []
        sents1 = split_sentences(text1)
        sents2 = split_sentences(text2)

        for s1 in sents1:
            for s2 in sents2:
                if sentence_similarity(preprocess(s1), preprocess(s2)) > 0.7:
                    plagiarized.append(s1)
                    break

        return {
            "similarity_score": round(doc_score * 100, 2),
            "plagiarism_level": level,
            "plagiarized_sentences": plagiarized,
        }

    except Exception as e:
        # IMPORTANT: This prevents silent 500 crashes
        raise HTTPException(status_code=500, detail=str(e))
