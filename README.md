# Plagiarism Checker Backend v3

Our system implements an internet-based plagiarism detection approach by querying publicly available web sources and applying NLP-based similarity analysis.

It follows the same detection pipeline but uses open-source and lightweight components suitable for academic use.

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
