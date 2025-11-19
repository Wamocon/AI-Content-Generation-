# AI Agent Instructions — FIAE AI Content Factory (DiTeLe)

Purpose: Make AI agents productive fast with the actual architecture, workflows, and conventions used here.

## Big Picture
- Generates German, DiTeLe‑standard training scenarios from Google Drive docs.
- Active entrypoint: `automation_ditele.py` (Phase 1). Phase 2 lives in `archived/phase2_components/` and is not active on `main`.
- Core flow: Drive → Analyze → Plan batches → Gemini generate → Build `.docx` → Upload → (optional) log to Sheets.

## Where Things Live
- `app/config.py`: Pydantic `Settings` reading `.env` (always use `settings.*`).
- `app/services/gemini_ai_service.py`: Low‑level Gemini client; rate‑limit 14/min, retries/backoff, primary `gemini-2.5-pro` → fallback `gemini-2.5-flash`; API `generate_content_with_retry(...)`.
- `app/services/intelligent_gemini_service.py`: High‑level wrapper (`generate_from_prompt(...)`, `generate_with_chunking(...)`).
- `app/services/document_analyzer.py`: Topic extraction, complexity score, content requirements with rule‑based fallback.
- `app/services/google_services.py`: Google Drive/Sheets via personal OAuth; reads `.docx` with `python-docx`; uploads to a per‑run Review subfolder; Sheets tab `Tabellenblatt1`.

## Run & Setup (Windows PowerShell)
```powershell
python -m venv .venv
 .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# OAuth (creates personal_google_token.pickle)
python personal_google_drive_service.py
```
`.env` (minimum): `GEMINI_API_KEY`, `GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID`, `GOOGLE_DRIVE_REVIEW_FOLDER_ID`, `PERSONAL_GOOGLE_ACCOUNT_ENABLED=True`, `LOG_LEVEL=INFO`.

## Orchestration (Phase 1)
- `automation_ditele.py` controls the batch; `TEST_MODE=True` limits to 2 docs; set `False` after review.
- Generates strict DiTeLe sections; multiple “PROBLEM n / LÖSUNG n” pairs; cleans/renumbers via `_cleanup_batch_content`.
- Adaptive batching via `_calculate_optimal_batch_sizes`; `.docx` written with `python-docx`; uploaded to Drive Review.

## Conventions & Gotchas
- Language is German (`settings.output_language='de'`); prompts/validation assume German.
- DiTeLe structure is strict: Themenliste, Lernziele, Theoretische Grundlagen (≥700–800 Wörter), Ausgangslage, Problem‑Lösungs‑Paare (je Thema), Lernziel‑Checkliste.
- Remove/avoid “KI/AI/Bot/Quality Score” in outputs; `_cleanup_batch_content` enforces this.
- Use provided services for Gemini; don’t call SDK directly; respect 14/min rate limit and timeouts.
- Drive uses personal OAuth only; missing `python-docx` or token prevents `.docx` read/upload.
- Never hardcode IDs/keys; always read via `app/config.py`.

## Minimal Examples
- Generate with wrapper:
```python
from app.services.intelligent_gemini_service import IntelligentGeminiService
svc = IntelligentGeminiService()
text = await svc.generate_from_prompt(prompt, content_type="use cases", timeout=180)
```
- Analyze first, then generate:
```python
from app.services.document_analyzer import DocumentAnalyzer
an = DocumentAnalyzer(gemini_service=svc.gemini_service)
analysis = await an.analyze_document(content, doc_name, use_ai=True)
```

## Archived
- `archived/phase2_components/`: FastAPI, Docker, RAG, multi‑agent orchestration. Reference only; do not wire into Phase 1.
