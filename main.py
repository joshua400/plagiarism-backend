from fastapi import FastAPI, UploadFile, File
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
    document2: UploadFile = File(...)
):
    text1 = (await document1.read()).decode("utf-8")
    text2 = (await document2.read()).decode("utf-8")

    doc_score = document_similarity(
        preprocess(text1),
        preprocess(text2)
    )

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
            if sentence_similarity(
                preprocess(s1),
                preprocess(s2)
            ) > 0.7:
                plagiarized.append(s1)
                break

    return {
        "similarity_score": round(doc_score * 100, 2),
        "plagiarism_level": level,
        "plagiarized_sentences": plagiarized
    }

