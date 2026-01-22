from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.plagiarism import router

app = FastAPI(title="Plagiarism Checker API v3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Plagiarism Checker API v3",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {"status": "running"}
