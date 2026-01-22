# Plagiarism Checker Backend v3

Internet-based plagiarism detection API using FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app:app --reload
```

## Endpoints

- `GET /health` - Health check
- `POST /check-plagiarism` - Check text for plagiarism

## Environment Variables

- `OPENSERP_URL` - URL for OpenSerp search API
