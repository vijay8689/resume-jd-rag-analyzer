# Resume AI Match Analyzer

A Streamlit-based RAG application that analyzes a resume against a job description, finds skill gaps, and provides evidence-backed recommendations.

## Features
- Resume upload for PDF, DOCX, and TXT
- Section-aware text extraction and chunking
- ChromaDB indexing with session isolation
- JD parsing with requirement extraction and normalization
- Deterministic matching and scoring engine
- AI reasoning via OpenAI-compatible XKIRO model when configured
- Plotly dashboard and exportable reports
- Privacy-conscious handling and secure file validation

## Tech Stack
- Python 3.11+
- Streamlit
- LangChain
- ChromaDB
- Sentence Transformers
- PyMuPDF
- python-docx
- Pydantic
- Plotly
- pytest

## Project Structure

```text
resume-jd-rag-analyzer/
├── Application.py
├── pages/
├── src/
├── config/
├── prompts/
├── tests/
├── .streamlit/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── Dockerfile
```

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables
Create a local `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

For Streamlit Cloud or shared hosting, configure `.streamlit/secrets.toml`:

```toml
XKIRO_API_KEY = "your-api-key"
```

## Run locally

```bash
streamlit run Application.py
```

## Tests

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

## Deployment notes
- Push repo to GitHub.
- Create a new Streamlit app.
- Point it to `Application.py`.
- Add `XKIRO_API_KEY` in Streamlit secrets.
- Deploy.

## Security and privacy
- Never commit `.env` or `.streamlit/secrets.toml`.
- Do not log raw resume or full JD content.
- Use file validation and temporary cleanup.

## Limitations
- OCR for scanned PDFs is not included in the initial implementation.
- Local filesystem persistence may not be durable across hosted restarts.

## Future enhancements
- Hosted vector store and persistence layer
- Better JD extraction heuristics
- User analytics and history export
