# AI Agent Instructions — FIAE AI Content Factory

Purpose: Enable AI coding agents to be productive quickly in this codebase by capturing architecture, workflows, conventions, and integration specifics actually used here.

## Big Picture
- Generates German, DiTeLe‑standard training scenarios from source documents in Google Drive.
- Active entrypoint: `automation_ditele.py` (Phase 1). Phase 2 API/Dashboard exists under `archived/phase2_components/` and is not active on `main`.
- Core flow: Google Drive → Analyze document → Plan dynamic content → Generate content with Gemini (single/multi‑pass) → Build Word (`.docx`) → Upload back to Drive → (optional) log to Google Sheets.

## Architecture (Where Things Live)
- `app/config.py` — Pydantic `Settings`; reads `.env`. Use `settings.*` (don’t hardcode API keys/model names).
- `app/models.py` — Pydantic schemas for future API use (no FastAPI app in `main`).
- `app/services/gemini_ai_service.py` — Low‑level Gemini client with:
  - Rate limiting (14 calls/min), retries, backoff, timeout handling.
  - Primary/fallback models from `settings` (`gemini-2.5-pro` → `gemini-2.5-flash`).
  - Main API: `generate_content_with_retry(content_type, document_content, context_query, timeout, max_retries)` — only `context_query` (the prompt) is actually used.
- `app/services/intelligent_gemini_service.py` — High‑level wrapper:
  - `generate_from_prompt(prompt, content_type, timeout, max_retries)`
  - `generate_with_chunking(prompt_template, document_content, analysis_data, ...)` for large docs (summary → enhance).
- `app/services/document_analyzer.py` — Extracts topics/themes, computes complexity and content requirements; AI‑assisted with robust rule‑based fallback.
- `app/services/google_services.py` — Google Drive + Sheets via PERSONAL OAuth only (service account fallback disabled):
  - Drive: list files, read `.docx` with `python-docx`, upload results into a per‑run folder in Review.
  - Sheets: optional processing log (German sheet name: `Tabellenblatt1`).

## How The Orchestration Works
- `automation_ditele.py` orchestrates end‑to‑end:
  - `TEST_MODE=True` limits to first 2 docs; set `TEST_MODE=False` for full batch.
  - Builds DiTeLe sections; generates multiple “PROBLEM n / LÖSUNG n” pairs; renumbers and cleans content (`_cleanup_batch_content`).
  - Adapts batches by complexity (`_calculate_optimal_batch_sizes`).
  - Writes `.docx` via `python-docx` and uploads to Review folder.

## Required Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Put Google OAuth client file at: personal_credentials.json
python personal_google_drive_service.py   # completes OAuth; creates personal_google_token.pickle
```
Create `.env` with at least:
```
GEMINI_API_KEY=...
GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=...
GOOGLE_DRIVE_REVIEW_FOLDER_ID=...
PERSONAL_GOOGLE_ACCOUNT_ENABLED=True
LOG_LEVEL=INFO
```

## Run The Batch
```powershell
# First do a 2-doc test run (required)
python automation_ditele.py
# After review, open automation_ditele.py and set TEST_MODE=False for full batch
```

## Conventions & Gotchas
- Language: German output (`settings.output_language='de'`); prompts and validations assume German.
- DiTeLe structure is strict: Themenliste, Lernziele, Theoretische Grundlagen (≥ ~700–800 words), Ausgangslage, Problem‑Lösungs‑Paare (one per topic), Lernziel‑Checkliste.
- Content cleanup: avoid “KI/AI/Bot” wording in outputs; code renames to neutral terms.
- Gemini calls: respect rate limit (14/min) and timeouts; reuse `GeminiAIService`/`IntelligentGeminiService` instead of raw SDK.
- Drive access: personal OAuth only; service account fallback is disabled. Missing `python-docx` or OAuth token causes `.docx` read/upload failures.
- Settings: always go through `app/config.py` `settings`; do not hardcode IDs/keys in code.

## Extending Safely (Examples)
- Generate with wrapper:
```python
from app.services.intelligent_gemini_service import IntelligentGeminiService
svc = IntelligentGeminiService()
text = await svc.generate_from_prompt(prompt, content_type="use cases", timeout=180)
```
- Analyze document then generate:
```python
from app.services.document_analyzer import DocumentAnalyzer
an = DocumentAnalyzer(gemini_service=svc.gemini_service)
analysis = await an.analyze_document(content, doc_name, use_ai=True)
```

## Archived Components
- `archived/phase2_components/` contains FastAPI, Docker, and orchestration variants used previously. Treat as reference; not wired into `main` flow.
