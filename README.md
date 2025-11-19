# FIAE AI Content Factory - DiTeLe Standard# FIAE AI Content Factory# FIAE AI Content Factory



**AI-Powered Educational Scenario Generation System**



[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)**AI-Powered Use Case Generation System****AI-Powered Use Case Generation System**

[![Status](https://img.shields.io/badge/status-production-green.svg)]()

[![DiTeLe](https://img.shields.io/badge/standard-DiTeLe-blue.svg)]()



---[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)



## 🎯 Quick Start (3 Steps)[![Status](https://img.shields.io/badge/status-production-green.svg)]()[![Status](https://img.shields.io/badge/status-production-green.svg)]()



```powershell

# 1. Test Mode (REQUIRED FIRST - processes only 2 documents)

python automation_ditele.py---## 🎯 Overview



# 2. Review generated documents in Google Drive



# 3. After approval, set TEST_MODE = False and run full batch## 🎯 OverviewAutomated generation of high-quality German use cases (Anwendungsfälle) from source documents using AI-powered analysis and intelligent content generation.

python automation_ditele.py

```



**⚠️ IMPORTANT**: Always test with 2 documents before running full automation!Automated generation of high-quality German use cases (Anwendungsfälle) from source documents using AI-powered analysis and intelligent content generation.### Key Features



---



## 🎓 What is DiTeLe Standard?### Key Features- 🧠 **AI-Powered Analysis**: Intelligent document understanding with Google Gemini



DiTeLe is a **standardized educational structure** for IT apprentice training scenarios in Germany. This system automatically generates DiTeLe-compliant educational scenarios from source documents.- 📊 **Dynamic Generation**: Adapts to document size (3-40+ use cases)



### **DiTeLe Structure (6 Sections)**- 🧠 **AI-Powered Analysis** - Intelligent document understanding with Google Gemini- ✅ **Quality Validation**: 6-point scoring system (0-100)



1. **Themenliste** (Topic List) - Overview of all topics covered- 📊 **Dynamic Generation** - Adapts to document size (3-40+ use cases)- 📁 **Google Drive Integration**: Seamless upload/download

2. **Lernziele** (Learning Objectives) - Measurable learning goals (upfront)

3. **Theoretische Grundlagen** (Theoretical Foundation) - Expanded theory (800+ words)- ✅ **Quality Validation** - 6-point scoring system (0-100)- 🎯 **Agentic Architecture**: 3 AI agents working autonomously

4. **Ausgangslage** (Starting Situation) - Realistic apprentice context

5. **Problem-Lösungs-Paare** (Problem-Solution Pairs) - One pair per topic with detailed steps- 📁 **Google Drive Integration** - Seamless upload/download- 📄 **Professional Output**: Formatted Word documents in German

6. **Lernziel-Checkliste** (Learning Objectives Checklist) - Verification questions

- 🎯 **Agentic Architecture** - 3 AI agents working autonomously

---

- 📄 **Professional Output** - Formatted Word documents in German## ⚡ Quick Start (3 Commands)

## 📋 Table of Contents



- [Features](#-features)

- [Installation](#-installation)---```powershell

- [Usage Guide](#-usage-guide)

- [Configuration](#-configuration)# 1. Start Docker containers

- [Output Examples](#-output-examples)

- [Architecture](#-architecture)## 🚀 Quick Startdocker-compose up -d

- [Troubleshooting](#-troubleshooting)

- [FAQ](#-faq)



---### Prerequisites# 2. Open Dashboard



## ✨ Features# Visit: http://localhost:3000



### **DiTeLe Compliance**- Python 3.11+

- ✅ **6-section standard structure** (Themenliste, Lernziele, Grundlagen, Ausgangslage, Problem-Lösungs-Paare, Checkliste)

- ✅ **Multiple problem-solution pairs** (one per topic, not a single comprehensive use case)- Google Cloud credentials# 3. Process Documents

- ✅ **Expanded theory section** (800+ words minimum, beginner-friendly explanations)

- ✅ **Professional formatting** (Arial Narrow font, proper headings, spacing)- Gemini API key# Click "Processing" → "Start Batch Processing"



### **Safety & Quality**- Virtual environment```

- ✅ **Test mode built-in** (processes only 2 documents by default)

- ✅ **Quality validation** (checks all 6 sections present)

- ✅ **Error handling** (retries, fallbacks, graceful degradation)

- ✅ **Comprehensive logging** (track every step)### Installation & Run**Access Points:**



### **AI-Powered**- **Dashboard**: http://localhost:3000

- 🧠 **Google Gemini 1.5 Pro** (advanced language understanding)

- 📊 **Intelligent document analysis** (topic extraction, complexity assessment)1. **Navigate to project**- **Backend API**: http://localhost:8000

- 🎯 **Content adaptation** (adjusts to document size and technical depth)

- ✅ **Rate limiting** (15-second pause between documents)- **API Docs**: http://localhost:8000/docs



### **Google Drive Integration**   ```powershell- **WebSocket**: ws://localhost:8000/ws

- 📁 **Automatic upload/download** (seamless workflow)

- 🔍 **Recursive subfolder search** (finds documents anywhere in source folder)   cd "d:\FIAE Agents with RAG"

# FIAE AI Content Factory — DiTeLe Standard

AI-powered system that generates German, DiTeLe-compliant training scenarios (Anwendungsfälle) from source `.docx` files in Google Drive. Output is a professionally formatted Word document uploaded back to Drive.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/) [![Status](https://img.shields.io/badge/status-production-green.svg)]() [![DiTeLe](https://img.shields.io/badge/standard-DiTeLe-blue.svg)]()

---

## Overview

End-to-end flow:

1) Google Drive source folder → 2) Document analysis (topics, complexity) → 3) Adaptive batching and prompt generation → 4) Gemini content generation → 5) `.docx` assembly (python-docx) → 6) Upload to Google Drive Review folder → 7) (Optional) log to Google Sheets.

Active entrypoint: `automation_ditele.py` (Phase 1). Phase 2 (API/Dashboard, RAG, multi-agent orchestration) is archived under `archived/phase2_components/` and not active on `main`.

---

## Repository Structure

```
AI-Content-Generation/
├─ automation_ditele.py                      # Main Phase 1 orchestrator (active)
├─ personal_google_drive_service.py          # Runs OAuth flow and stores personal token
├─ requirements.txt                          # Python dependencies
├─ pyproject.toml                            # Tooling/format config (if used)
├─ app/
│  ├─ config.py                              # Pydantic Settings; reads .env (use settings.*)
│  ├─ models.py                              # Pydantic models (future API use)
│  └─ services/
│     ├─ gemini_ai_service.py                # Low-level Gemini client (rate-limit, retries)
│     ├─ intelligent_gemini_service.py       # High-level wrapper (generate_from_prompt, chunking)
│     ├─ document_analyzer.py                # Topic extraction, complexity, requirements
│     └─ google_services.py                  # Google Drive & Sheets integration (personal OAuth)
└─ archived/
   ├─ README.md                              # What’s archived and why
   ├─ automation_*.py                        # Old Phase 1/2 scripts (reference only)
   └─ phase2_components/                     # FastAPI, Docker, RAG, orchestrators (inactive)
```

---

## Setup (Windows PowerShell)

Prerequisites: Python 3.11+, Google API OAuth client credentials, Gemini API key.

```powershell
python -m venv .venv
 .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env in the repo root (minimum):
# GEMINI_API_KEY=...
# GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=...
# GOOGLE_DRIVE_REVIEW_FOLDER_ID=...
# PERSONAL_GOOGLE_ACCOUNT_ENABLED=True
# LOG_LEVEL=INFO

# Run OAuth (stores personal_google_token.pickle after browser flow)
python personal_google_drive_service.py
```

Important:
- Use personal OAuth only (service account is not used in Phase 1).
- Do not hardcode keys/IDs in code; always read via `app/config.py` `settings`.

---

## How It Works

`automation_ditele.py` orchestrates the full batch:

- Reads Drive source folder (ID in `.env`).
- Loads each `.docx`, extracts plain text, and analyzes it with `DocumentAnalyzer` to get topics and complexity.
- Plans adaptive batches via `_calculate_optimal_batch_sizes` based on complexity.
- Builds DiTeLe-compliant prompts and generates content with `IntelligentGeminiService` (internally uses `GeminiAIService` with 14/min rate limiting and retries/backoff).
- Cleans and renumbers content (`_cleanup_batch_content`) to enforce forbidden-term removal and consistent numbering of “PROBLEM n / LÖSUNG n”.
- Assembles a Word document using `python-docx` and uploads to the Review folder.

DiTeLe sections produced:
1. Themenliste
2. Lernziele (vorne)
3. Theoretische Grundlagen (≥700–800 Wörter)
4. Ausgangslage
5. Problem‑Lösungs‑Paare (je Thema ein Paar)
6. Lernziel‑Checkliste

Output naming: `DiTeLe_Szenario_{original_doc_name}_{YYYYMMDD_HHMMSS}.docx`.

---

## Run

Test Mode (required first run):

```powershell
python automation_ditele.py
```

What happens:
- Processes only the first 2 documents from the source folder (`TEST_MODE=True`).
- Builds and uploads 2 DiTeLe-compliant `.docx` files to the Review folder.

Full Batch:

```powershell
# Open automation_ditele.py and set TEST_MODE=False, then:
python automation_ditele.py
```

Review the output in the Review folder before running full batches.

---

## Configuration

Key `.env` variables (minimum):

- `GEMINI_API_KEY`: Gemini API key.
- `GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID`: Drive folder containing source `.docx` documents.
- `GOOGLE_DRIVE_REVIEW_FOLDER_ID`: Drive folder where generated `.docx` are uploaded.
- `PERSONAL_GOOGLE_ACCOUNT_ENABLED=True`: Use personal OAuth (created by `personal_google_drive_service.py`).
- `LOG_LEVEL`: e.g., `INFO`.

All settings are read via `app/config.py` (`from app.config import settings`).

---

## Key Services (when extending)

- `GeminiAIService` (`app/services/gemini_ai_service.py`): Low-level client with rate limiting (14/min), retries, and fallback model (`gemini-2.5-pro` → `gemini-2.5-flash`). Prefer using the high-level wrapper below.
- `IntelligentGeminiService` (`app/services/intelligent_gemini_service.py`):
  - `generate_from_prompt(prompt, content_type, timeout=...)`
  - `generate_with_chunking(prompt_template, document_content, analysis_data, ...)`
- `DocumentAnalyzer` (`app/services/document_analyzer.py`): `analyze_document(content, doc_name, use_ai=True)` returns topics, complexity, and content requirements with rule-based fallback.
- `GoogleDriveService` (`app/services/google_services.py`): Lists/reads `.docx`, uploads results, optional Sheets logging (tab `Tabellenblatt1`).

Minimal example:

```python
from app.services.intelligent_gemini_service import IntelligentGeminiService
from app.services.document_analyzer import DocumentAnalyzer

svc = IntelligentGeminiService()
an = DocumentAnalyzer(gemini_service=svc.gemini_service)
analysis = await an.analyze_document(content, "Beispiel.docx", use_ai=True)
text = await svc.generate_from_prompt("Schreibe Lernziele …", content_type="use cases", timeout=180)
```

---

## Conventions & Gotchas

- Output language is German; prompts and validators assume German.
- Strict DiTeLe structure and quality gates; solutions must be complete step‑by‑step and beginner‑friendly.
- Forbidden wording (e.g., “Bot”, “KI/AI”, “Quality Score”) is removed by `_cleanup_batch_content`.
- Use built services; do not call raw Gemini SDK directly.
- Missing `python-docx` or OAuth token prevents `.docx` I/O and uploads.

---

## Troubleshooting

- OAuth issues: Re-run `python personal_google_drive_service.py` and ensure `personal_google_token.pickle` exists.
- 403/404 Drive errors: Verify folder IDs in `.env` and personal account access.
- Rate limiting/timeouts: Calls are auto-retried; large documents may need more time.
- Empty output: Check logs (Loguru to stdout) and confirm source file actually contains parsable text.

---

## Archived (Reference Only)

`archived/` and `archived/phase2_components/` include the previous API/Dashboard, RAG, and multi-agent orchestration. They are not part of the active Phase 1 flow. See the READMEs in those folders if you plan a Phase 2 revival.

---

## License

Internal project. If you plan to open-source, add a suitable license file.

```

FR-659.docx (3,500 words)| 1,000 words  | 3         | ~6 minutes      |

Topics: Python, Flask, REST APIs, PostgreSQL, Frontend

```| 3,000 words  | 5         | ~10 minutes     |**Total Generated**: ~150 pages of professional educational material



### **Generated Output**| 6,000 words  | 10        | ~16 minutes     |



```| 12,000 words | 20        | ~31 minutes     |**Processing Time**: 60-120 seconds

DiTeLe_Szenario_FR-659_20251118_143022.docx (12-16 pages)



Structure:

├── Themenliste (1 page)### Quality Distribution---

│   • Python Programming

│   • Flask Web Framework- **EXCELLENT (90-100):** 60%

│   • REST API Development

│   • PostgreSQL Integration- **GOOD (75-89):** 30%## 🔧 Installation & Setup

│   • Frontend Development

│- **ACCEPTABLE (60-74):** 8%

├── Lernziele (1 page)

│   • Flask-Anwendungen erstellen können- **NEEDS_IMPROVEMENT (<60):** 2%### **Prerequisites**

│   • REST APIs implementieren und testen

│   • Mit Datenbanken arbeiten (CRUD)- Docker Desktop installed and running

│   • MVC-Pattern anwenden

│   • Unit Tests schreiben---- Git (for cloning)

│

├── Theoretische Grundlagen (3-4 pages)- Google Cloud credentials (optional, for Google Drive integration)

│   • Python: 200 words

│   • Flask: 200 words## 🔧 Configuration- Gemini API key (for AI content generation)

│   • REST APIs: 200 words

│   • PostgreSQL: 200 words

│   • Frontend: 200 words

│Key environment variables in `.env`:### **Method 1: Docker (Recommended)**

├── Ausgangslage (1 page)

│   Azubi Max arbeitet bei IT-Solutions GmbH...

│   Projekt: Kundenverwaltungs-Webanwendung...

│```env```powershell

├── Problem-Lösungs-Paare (6-8 pages)

│   Problem 1: Flask Setup# Required   ```powershell

│   Lösung 1: Schritt 1, 2, 3... (detailed)

│   GEMINI_API_KEY=your_gemini_api_key   cd "d:\FIAE Agents with RAG"

│   Problem 2: REST API Implementierung

│   Lösung 2: Schritt 1, 2, 3... (detailed)GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=source_folder_id   ```

│   

│   [... one pair per topic ...]GOOGLE_DRIVE_REVIEW_FOLDER_ID=review_folder_id

│

└── Lernziel-Checkliste (1 page)GOOGLE_APPLICATION_CREDENTIALS=credentials/file.json2. **Activate environment**

    ☐ Kann ich Flask-Anwendungen erstellen?

    ☐ Kann ich REST APIs implementieren?

    ☐ Kann ich mit Datenbanken arbeiten?

    [...]# Optional   ```powershell

```

LOG_LEVEL=INFO   .\.venv\Scripts\Activate.ps1

---

```   ```

## 🏗️ Architecture



### **System Components**

---3. **Configure .env**

```

┌─────────────────────────────────────────────────────────┐

│              automation_ditele.py                       │

│                                                         │## 📖 Documentation   ```bash

│  1. Document Discovery                                  │

│     └─> GoogleDriveService.list_files_in_folder()     │   # Add to .env file:

│                                                         │

│  2. Document Analysis                                   │**Complete documentation:** `DOCUMENTATION.md`   GEMINI_API_KEY=your_key

│     └─> DocumentAnalyzer.analyze()                     │

│         • Topic extraction                             │   GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=your_folder_id

│         • Complexity assessment                        │

│         • Content requirements                         │Includes:   GOOGLE_DRIVE_REVIEW_FOLDER_ID=your_folder_id

│                                                         │

│  3. DiTeLe Generation                                   │- Detailed architecture explanation   ```

│     └─> IntelligentGeminiService.generate_with_retry() │

│         • 3500+ character DiTeLe-compliant prompt      │- API reference

│         • Multiple problem-solution pairs              │

│         • Expanded theory section                      │- Configuration guide4. **Run automation**

│                                                         │

│  4. Structure Validation                                │- Troubleshooting

│     └─> validate_ditele_structure()                    │

│         • Check 6 required sections                    │- Archived components information   ```powershell

│         • Warn if any missing                          │

│                                                         │   python automation_phase1_content.py

│  5. Word Document Creation                              │

│     └─> create_ditele_word_document()                  │---   ```

│         • Arial Narrow font                            │

│         • Professional formatting                      │

│         • Metadata table                               │

│                                                         │## 🗂️ Archived Components### Expected Output

│  6. Upload to Google Drive                              │

│     └─> GoogleDriveService.upload_file()               │

│                                                         │

└─────────────────────────────────────────────────────────┘Components for Phase 2 (presentations, quizzes) are archived in `archived_phase2_components/`:```



External Services:- 7 unused services🚀 PHASE 1: ANWENDUNGSFÄLLE-GENERIERUNG

├── Google Gemini 1.5 Pro (AI generation)

├── Google Drive API (file management)- FastAPI web server📚 5 Dokumente gefunden

└── python-docx (Word formatting)

```- Docker configuration[1/5] VERARBEITE: document1.docx



### **Key Services** (`app/services/`)- Old automation files   🧠 Analysiere Dokument... (10 Anwendungsfälle empfohlen)



1. **`google_services.py`** - Google Drive integration (OAuth2 + Service Account)   🤖 Generiere Anwendungsfälle...

2. **`intelligent_gemini_service.py`** - Gemini AI with rate limiting, retries, error handling

3. **`document_analyzer.py`** - Document analysis, topic extraction, requirements calculationSee `archived_phase2_components/README.md` for restoration instructions.   🔍 Qualität: 92/100 (EXCELLENT)

4. **`gemini_ai_service.py`** - Base Gemini service wrapper

   ✅ ERFOLG!

---

---🎉 VERARBEITUNG ABGESCHLOSSEN

## 🔧 Troubleshooting

```

### **Problem: "Too many API requests"**

## 🛠️ Troubleshooting

**Symptoms:**

```# 2. Configure environment

ERROR: Gemini API rate limit exceeded

```**Import errors:**# Create .env file in root directory



**Solution:**```powershellcopy env.example .env

Increase pause time between documents:

pip install -r requirements.txt# Edit .env with your settings

```python

# Edit automation_ditele.py, line 965:```

await asyncio.sleep(30)  # Increased from 15 to 30 seconds

```# 3. Build and start



---**Google Drive connection failed:**docker-compose build



### **Problem: "DiTeLe structure validation failed"**- Check `.env` credentialsdocker-compose up -d



**Symptoms:**- Verify folder IDs

```

⚠️ WARNUNG: DiTeLe-Struktur unvollständig- Ensure `credentials/` has JSON file# 4. Check status

Fehlende Abschnitte: ['Theoretische Grundlagen']

```docker ps



**Solution:****Gemini API errors:**# Should show: fiae-backend (healthy), fiae-frontend (healthy)

This is a warning, not an error. The document is still generated but may be incomplete. Check:

1. Source document has enough content- Verify `GEMINI_API_KEY` in `.env`

2. Gemini API is responding correctly

3. Review generated document manually- Check API quota/rate limits# 5. Access dashboard



---- System has automatic retry (3 attempts)# Open: http://localhost:3000



### **Problem: "Google Drive authentication failed"**```



**Symptoms:**---

```

[CRITICAL] Google services initialization failed### **Method 2: Manual Setup**

```

## 📌 Quick Reference

**Solution:**

```powershell```powershell

# Delete existing token

Remove-Item personal_google_token.pickle**Main command:**# Backend



# Re-authenticate```powershellpip install -r requirements.txt

python personal_google_drive_service.py

python automation_phase1_content.pypython -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Follow browser prompts

``````



---# Frontend (new terminal)



### **Problem: "Font not applied correctly"****Key files:**cd frontend



**Symptoms:**- Main: `automation_phase1_content.py`npm install

Generated Word documents don't use Arial Narrow font.

- Config: `.env`, `app/config.py`npm run dev

**Solution:**

Arial Narrow must be installed on your system:- Docs: `DOCUMENTATION.md````

1. Check if font is installed: Open Word → Font dropdown → Search "Arial Narrow"

2. If missing, download and install Arial Narrow font

3. Re-run automation

**Google Drive folders:**---

---

- Source: `1YtN3_CftdJGgK9DFGLSMIky7PbYfFsX5`

### **Problem: "No documents found"**

- Review: `1fBJdZKHLR-5jxfwKj8RLG45rKyZU8cXb`## ⚙️ Configuration

**Symptoms:**

```

📚 0 Dokumente gefunden

```---### **Required Environment Variables**



**Solution:**

```powershell

# Check source folder ID in .env## ✅ System StatusCreate `.env` in root directory:

GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=...



# Verify folder contains DOCX files

# Script searches recursively in subfolders- **Status:** Production-ready ✅```bash



# Check Google Drive folder permissions- **Version:** 2.0 (Phase 1)# Core Settings

# Service account must have "Viewer" or "Editor" access

```- **Python:** 3.11.9ENVIRONMENT=production



---- **Last Updated:** November 11, 2025API_HOST=0.0.0.0



## ❓ FAQAPI_PORT=8000



### **Q: How long does it take to process 100 documents?**---LOG_LEVEL=INFO



**A:** 8-10 hours total. Each document takes ~5-6 minutes (analysis + generation + upload + 15-second pause).



---**For complete documentation, see `DOCUMENTATION.md`**# Google Services (Optional - for Google Drive integration)



### **Q: Can I process PDFs instead of DOCX?**GOOGLE_CREDENTIALS_PATH=credentials/your-service-account.json

GOOGLE_DRIVE_FOLDER_ID=your_source_folder_id

**A:** Currently only DOCX is supported. To add PDF support, modify `GoogleDriveService.download_document()` to extract text from PDFs.GOOGLE_DRIVE_REVIEW_FOLDER_ID=your_review_folder_id

GOOGLE_SHEETS_ID=your_tracking_sheet_id

---

# AI Services (Required)

### **Q: What if a document fails during processing?**GEMINI_API_KEY=your_gemini_api_key_here



**A:** The system logs the error and continues with the next document. Failed documents are tracked in logs. You can re-run automation for failed documents only.# CORS

ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

---```



### **Q: Can I customize the DiTeLe prompt?**Create `frontend/.env.local`:



**A:** Yes! Edit `automation_ditele.py`, line 99-171 (`_generate_problem_solution_template()` function) to modify the generation prompt.```bash

NEXT_PUBLIC_API_URL=http://localhost:8000

---NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

BACKEND_URL=http://backend:8000

### **Q: How do I know if quality is good enough?**WS_URL=ws://backend:8000/ws

```

**A:** Use the quality checklist in the Usage Guide section. Show 2-3 test documents to stakeholders (Nikolaj, Erwin, Waleri) for approval before full run.

---

---

## 📖 Usage Guide

### **Q: Can I run automation overnight?**

### **Dashboard Features**

**A:** Yes! Set `TEST_MODE = False` and run in a screen/tmux session or use PowerShell job:

#### **Main Dashboard**

```powershell- System health status

Start-Job -ScriptBlock { python automation_ditele.py }- Active jobs counter

```- Documents processed

- Service status panel

---- Real-time updates



### **Q: What's the difference between old system and DiTeLe?**#### **Processing Page**

1. Click "Discover Documents" to scan Google Drive

| Feature | Old System | DiTeLe System |2. Click "Start Batch Processing" to begin automation

|---------|-----------|---------------|3. Monitor real-time progress via WebSocket

| **Structure** | 5 sections | 6 sections (DiTeLe) |4. Check results in Google Drive review folder

| **Use Cases** | 1 comprehensive | Multiple problem-solution pairs |

| **Theory** | Compressed | Expanded (800+ words) |#### **Agents Page**

| **Learning Objectives** | At end only | At start + end (checklist) |- View all 6 CrewAI agents

| **File** | `archived/automation_phase1_content.py` | `automation_ditele.py` |- Start individual agent workflows

- Monitor agent collaboration

---- Track task completion



## 📁 Project Structure#### **RAG Page**

- Vector database status

```- Document embedding count

FIAE Agents with RAG/- Process documents with RAG

├── automation_ditele.py            ⭐ MAIN FILE (DiTeLe generation)- Reset knowledge base

├── personal_google_drive_service.py   OAuth2 setup script

├── README.md                       ⭐ This file#### **Monitoring Page**

├── requirements.txt                   Python dependencies- System metrics

├── pyproject.toml                     Python project config- Performance graphs

├── .env                               Configuration (not committed)- Active alerts

├── env.example                        Configuration template- Error tracking

│

├── app/                            ⭐ CORE SERVICES---

│   ├── config.py                      Settings management

│   ├── models.py                      Data models## 📂 Project Structure

│   └── services/

│       ├── google_services.py         Google Drive/Sheets```

│       ├── intelligent_gemini_service.py  Gemini AIFIAE Agents with RAG/

│       ├── document_analyzer.py       Document analysis├── app/                                # Backend FastAPI application

│       └── gemini_ai_service.py       Base Gemini service│   ├── main.py                         # Main API application (2205 lines)

││   ├── config.py                       # Settings management

├── credentials/                       Google API credentials│   ├── models.py                       # Pydantic data models

│   ├── README.md│   └── services/                       # AI & integration services

│   └── wmc-automation-agents-*.json   Service account│       ├── rag_enhanced_processor.py   # RAG + Gemini processor (627 lines)

││       ├── crewai_orchestrator.py      # Multi-agent system (389 lines)

├── chroma_db/                         Vector database (unused)│       ├── langgraph_orchestrator.py   # Workflow management (365 lines)

├── logs/                              Application logs│       ├── advanced_document_processor.py # Document extraction (285 lines)

├── temp/                              Temporary files│       ├── google_services.py          # Google Drive/Sheets (396 lines)

││       ├── gemini_ai_service.py        # Gemini AI service

└── archived/                       📦 DEPRECATED CODE│       ├── content_intelligence.py     # Content analysis

    ├── README.md                      Archive documentation│       └── production_monitor.py       # System monitoring

    ├── automation_phase1_content.py   Old single use case system│

    ├── automation_phase2_presentation.py  Presentation generation├── frontend/                           # Next.js 14 application

    ├── automation_engine.py           Old comprehensive engine│   ├── src/

    └── phase2_components/             Phase 2 system (Docker, APIs, etc.)│   │   ├── app/                        # App router pages

```│   │   │   ├── page.tsx                # Main dashboard

│   │   │   ├── processing/            # Processing queue

---│   │   │   ├── agents/                # Agent workflows

│   │   │   ├── rag/                   # RAG management

## 📈 Performance Metrics│   │   │   ├── monitoring/            # System monitoring

│   │   │   ├── analytics/             # Analytics

### **Processing Time**│   │   │   └── review/                # HITL review

│   │   ├── components/                # React components (20+)

| Document Size | Analysis | Generation | Upload | Total |│   │   ├── services/

|---------------|----------|------------|--------|-------|│   │   │   ├── api-client.ts          # API service layer (450 lines)

| Small (1,000 words) | 15s | 3-4 min | 5s | ~4 min |│   │   │   └── websocket.ts           # WebSocket client

| Medium (3,000 words) | 20s | 4-5 min | 10s | ~5 min |│   │   └── hooks/                     # Custom React hooks

| Large (5,000+ words) | 30s | 5-6 min | 15s | ~6 min |│   │       ├── useApi.ts

│   │       └── useWebSocket.ts

**Plus:** 15-second mandatory pause between documents│   └── package.json

│

### **Success Rate**├── automation_engine.py                # Main automation script (393 lines)

├── personal_google_drive_service.py    # OAuth2 personal account

- **Test Mode (2 docs):** 100% expected├── credentials/                        # Google credentials

- **Full Run (100 docs):** 95-98% typical│   ├── README.md

- **Failures:** Usually due to API rate limits or malformed source documents│   └── wmc-automation-agents-*.json    # Service account

├── chroma_db/                          # Vector database storage

### **Resource Usage**├── logs/                               # Application logs

├── docker-compose.yml                  # Production config

- **RAM:** ~500 MB (Python process)├── docker-compose.dev.yml              # Development config

- **Disk:** ~1 MB per generated document├── Dockerfile.backend                  # Backend image

- **Network:** ~2 MB upload per document├── Dockerfile.frontend                 # Frontend image

- **API Calls:** ~8-10 Gemini calls per document├── requirements.txt                    # Python dependencies

├── pyproject.toml                      # Python project config

---├── .env.example                        # Environment template

├── build_and_start.ps1                 # Build automation script

## 🔒 Security└── README.md                           # This file

```

### **Credential Files (DO NOT COMMIT)**

---

- `personal_credentials.json` - OAuth2 client secrets

- `personal_google_token.pickle` - OAuth2 access tokens## 🎯 Content Generation Formula

- `credentials/wmc-automation-agents-*.json` - Service account key

- `.env` - Environment variables| Content Type | Formula | Min | Max | Example (5000 words) |

|--------------|---------|-----|-----|----------------------|

### **Best Practices**| **PowerPoint Slides** | words ÷ 150 | 10 | 50 | 33 slides |

| **Google Slides** | Same as PPT | 10 | 50 | 33 slides |

- ✅ Use `.gitignore` to exclude credentials| **Use Case Pages** | words ÷ 400 | 3 | 20 | 12 pages |

- ✅ Rotate API keys quarterly| **Quiz Questions** | words ÷ 100 | 10 | 50 | 50 questions |

- ✅ Use service accounts for automation (not personal accounts)| **Trainer Script** | 1 page/slide | 10 | 50 | 33 pages |

- ✅ Restrict Google Drive folder permissions (least privilege)

- ✅ Enable 2FA on Google accounts---

- ✅ Monitor API usage in Google Cloud Console

## 🤖 AI Processing Pipeline

---

### **Phase 1: Content Extraction**

## 🚢 Deployment- Full text extraction from DOCX

- Image extraction with metadata

### **Development Environment**- Table extraction with formatting

- Metadata collection

```powershell

# Run locally with virtual environment### **Phase 2: Depth Analysis**

.\.venv\Scripts\Activate.ps1- Word count calculation

python automation_ditele.py- Topic density assessment

```- Required output sizing (n-number)

- Content complexity evaluation

### **Production Environment**

### **Phase 3: RAG Enhancement**

```powershell- Document chunking (1000 chars, 200 overlap)

# Run in background job (overnight)- Embedding generation (Sentence Transformers)

Start-Job -ScriptBlock { - Vector storage (ChromaDB)

    cd "d:\FIAE Agents with RAG"- Semantic search preparation

    .\.venv\Scripts\Activate.ps1

    python automation_ditele.py### **Phase 4: Content Generation**

}- **CrewAI Multi-Agent Collaboration**:

  - Agent 1: Analyzes content, extracts knowledge

# Check job status  - Agent 2: Creates PowerPoint & Google Slides

Get-Job  - Agent 3: Develops IT use cases with solutions

  - Agent 4: Generates multi-difficulty quizzes

# Get job output  - Agent 5: Writes trainer scripts

Receive-Job -Id 1  - Agent 6: Validates quality & completeness

```

### **Phase 5: Quality Assurance**

### **Scheduled Task (Windows)**- Completeness validation (100% coverage check)

- Content quality scoring

```powershell- Format verification

# Create scheduled task to run daily at 6 AM- Error detection

$action = New-ScheduledTaskAction -Execute "python" -Argument "automation_ditele.py" -WorkingDirectory "d:\FIAE Agents with RAG"

$trigger = New-ScheduledTaskTrigger -Daily -At 6am---

Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DiTeLe Automation" -Description "Daily DiTeLe scenario generation"

```## 📱 API Endpoints



---### **System Health**

- `GET /health` - Basic health check

## 🧪 Testing- `GET /monitoring/health` - Detailed health metrics

- `GET /monitoring/metrics` - System performance metrics

### **Syntax Validation**

### **Document Processing**

```powershell- `POST /process-document` - Process single document

python -m py_compile automation_ditele.py- `POST /process-document-upload` - Upload & process

```- `POST /process-comprehensive-batch` - Batch processing

- `POST /process-document-rag` - RAG-enhanced processing

### **Test Mode**- `POST /process-document-orchestrated` - LangGraph orchestration



```powershell### **Batch Operations**

# Processes only 2 documents- `GET /discover-documents` - Scan Google Drive folder

python automation_ditele.py- `GET /batch-status` - Current batch status

```- `POST /abort-automation/{job_id}` - Cancel running job



### **Dry Run (no upload)**### **AI Services**

- `GET /crewai/status` - CrewAI agent status

Edit `automation_ditele.py`, comment out upload:- `POST /crewai/run-workflow` - Start agent workflow

- `GET /rag/status` - RAG system status

```python- `POST /rag/reset` - Reset knowledge base

# Line ~830

# uploaded_file = await google_drive_service.upload_file(...)### **Monitoring**

logger.info("   [DRY RUN] Skipped upload")- `GET /production-monitor/status` - System status

```- `GET /production-monitor/metrics` - Performance metrics

- `GET /production-monitor/alerts` - Active alerts

---

### **Real-time**

## 📚 Documentation- `WS /ws` - WebSocket for live updates



- **Main Documentation**: This README**Full API Documentation**: http://localhost:8000/docs

- **Archive Documentation**: `archived/README.md`

- **Environment Template**: `env.example`---

- **Credentials Setup**: `credentials/README.md`

## 🔍 Monitoring & Debugging

---

### **Health Checks**

## 🎓 Learning Resources

```powershell

### **DiTeLe Standard**# Backend health

- Ask Nikolaj, Erwin, or Waleri for official DiTeLe documentationcurl http://localhost:8000/health

- Reference: Stakeholder feedback from November 2025

# Frontend health

### **Technologies Used**curl http://localhost:3000

- **Python**: https://docs.python.org/3.11/

- **Google Gemini**: https://ai.google.dev/docs# Docker container status

- **Google Drive API**: https://developers.google.com/drivedocker ps

- **python-docx**: https://python-docx.readthedocs.io

# View logs

---docker logs fiae-backend

docker logs fiae-frontend

## 🤝 Contributing```



This is an internal project. For changes:### **Common Issues & Solutions**



1. Create feature branch: `git checkout -b feature/description`#### **Problem**: Containers won't start

2. Test thoroughly with TEST_MODE = True```powershell

3. Commit with clear messages: `git commit -m "Add feature: description"`# Solution 1: Check if ports are available

4. Push and create PR: `git push origin feature/description`netstat -ano | findstr :8000

netstat -ano | findstr :3000

---

# Solution 2: Restart Docker Desktop

## 📞 Support# Close Docker Desktop → Restart



- **Technical Issues**: Check logs in `logs/` directory# Solution 3: Rebuild containers

- **Quality Issues**: Review with Nikolaj, Erwin, Waleridocker-compose down

- **API Issues**: Check Google Cloud Console (API quotas, billing)docker-compose build --no-cache

docker-compose up -d

---```



## ✅ Pre-Flight Checklist#### **Problem**: Frontend can't connect to backend

```bash

Before running automation:# Check backend is running

docker ps | grep fiae-backend

- [ ] Python 3.11+ installed

- [ ] Virtual environment activated# Check environment variables

- [ ] `.env` file configured (Gemini API key, folder IDs)docker exec fiae-frontend env | grep NEXT_PUBLIC

- [ ] Google credentials in place (`credentials/`, `personal_google_token.pickle`)

- [ ] Source folder has DOCX documents# Verify in frontend/.env.local:

- [ ] Review folder accessibleNEXT_PUBLIC_API_URL=http://localhost:8000

- [ ] TEST_MODE = True (for first run)NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

- [ ] Stable internet connection```



---#### **Problem**: Content generation fails

```bash

## 📊 System Status# Check Gemini API key

docker exec fiae-backend env | grep GEMINI_API_KEY

| Component | Status | Version |

|-----------|--------|---------|# Check logs for errors

| **DiTeLe System** | ✅ Production Ready | 1.0.0 |docker logs fiae-backend | grep -i error

| **Python** | ✅ 3.11.9 | 3.11+ |

| **Google Gemini** | ✅ Configured | 1.5 Pro |# Verify API quota at Google Cloud Console

| **Google Drive** | ✅ Integrated | API v3 |```

| **python-docx** | ✅ Active | 1.1.0+ |

#### **Problem**: OAuth2 authentication fails

---```bash

# Solution:

## 🎉 Success Metrics# 1. Delete token file

rm personal_google_token.pickle

After full automation run:

# 2. Re-run authentication

- **Documents Processed**: X of Y successfullypython personal_google_drive_service.py

- **Success Rate**: 95-98% typical

- **Total Time**: 8-10 hours for 100 documents# 3. Complete browser authentication

- **Generated Content**: 12-16 pages per document

- **Quality**: Stakeholder-approved (Nikolaj, Erwin, Waleri)# 4. Restart containers

docker-compose restart

---```



## 🔄 Version History---



- **v1.0.0** (November 18, 2025) - DiTeLe standard implementation## 🔒 Security

  - 6-section DiTeLe structure

  - Multiple problem-solution pairs### **Credential Files (Protected)**

  - Expanded theory section (800+ words)

  - Test mode (2 documents first)**DO NOT DELETE OR COMMIT:**

  - Professional Word formatting (Arial Narrow)- `personal_credentials.json` - OAuth2 client credentials

  - Comprehensive error handling- `personal_google_token.pickle` - OAuth2 access tokens

- `credentials/wmc-automation-agents-*.json` - Service account key

- **v0.x** (Archived) - Old single use case system

  - See `archived/` for historical code### **Environment Variables**

- Never commit `.env` files

---- Use `.env.example` as template

- Rotate API keys regularly

## 🚀 Ready to Start?- Use service accounts for automation



1. ✅ Complete installation steps### **Best Practices**

2. ✅ Configure `.env` file- Enable 2FA on Google accounts

3. ✅ Run test mode: `python automation_ditele.py`- Restrict service account permissions

4. ✅ Review 2 generated documents- Use HTTPS in production

5. ✅ Get stakeholder approval- Implement rate limiting

6. ✅ Set `TEST_MODE = False`- Monitor API usage

7. ✅ Run full automation

8. ✅ Celebrate! 🎉---



---## 📈 Performance



**Built with ❤️ for intelligent educational content creation**### **Expected Performance**

- **Small docs** (1000 words): ~45 seconds

*Last Updated: November 18, 2025 | Version 1.0.0 - DiTeLe Standard Edition*- **Medium docs** (3000 words): ~75 seconds

- **Large docs** (5000+ words): ~120 seconds

---

### **Resource Requirements**

**Questions? Check the FAQ section or review logs in `logs/` directory.** 📖- **RAM**: 2-3 GB total (backend + frontend)

- **CPU**: 2+ cores recommended
- **Disk**: 500 MB + ~100 MB per 100 documents (ChromaDB)
- **Network**: Stable internet for Gemini API

### **Optimization Tips**
1. Process documents during off-peak hours
2. Clean ChromaDB monthly (`POST /rag/reset`)
3. Monitor Docker container resources
4. Keep dependencies updated
5. Use SSD for ChromaDB storage

---

## 🐳 Docker Commands

```powershell
# Start system
docker-compose up -d

# Stop system
docker-compose down

# Restart system
docker-compose restart

# View logs (all)
docker-compose logs -f

# View logs (backend only)
docker-compose logs -f backend

# View logs (frontend only)
docker-compose logs -f frontend

# Rebuild after code changes
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker ps

# Access container shell
docker exec -it fiae-backend bash
docker exec -it fiae-frontend sh

# View resource usage
docker stats
```

---

## 🛠️ Development

### **Backend Development**

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run specific service
python automation_engine.py

# Test RAG system
python -c "from app.services.rag_enhanced_processor import RAGEnhancedProcessor; print('RAG OK')"

# Test CrewAI
python -c "from app.services.crewai_orchestrator import CrewAIOrchestrator; print('CrewAI OK')"
```

### **Frontend Development**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

---

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **API Reference**: `docs/API.md`
- **OAuth Setup**: `docs/PERSONAL_GOOGLE_SETUP.md`

---

## ✅ Pre-Flight Checklist

Before processing documents:

- [ ] Docker Desktop is running
- [ ] Backend container is healthy (`docker ps`)
- [ ] Frontend container is healthy (`docker ps`)
- [ ] Dashboard loads at http://localhost:3000
- [ ] Backend responds at http://localhost:8000/health
- [ ] WebSocket connects (green indicator on dashboard)
- [ ] `.env` file configured with Gemini API key
- [ ] Google credentials in place (if using Drive)
- [ ] Source folder has DOCX documents

---

## 🎓 Learning Resources

### **Key Technologies**
- **FastAPI**: https://fastapi.tiangolo.com
- **Next.js**: https://nextjs.org
- **CrewAI**: https://docs.crewai.com
- **LangGraph**: https://langchain-ai.github.io/langgraph
- **ChromaDB**: https://docs.trychroma.com
- **Gemini AI**: https://ai.google.dev

### **Understanding the System**
1. **LangGraph**: State-based workflow orchestration
2. **CrewAI**: Multi-agent task collaboration
3. **RAG**: Retrieval-Augmented Generation for context
4. **Gemini 1.5 Pro**: Google's advanced language model

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: support@your-domain.com

---

## 🎉 Acknowledgments

Special thanks to:
- **FastAPI** team for the amazing web framework
- **Next.js** team for the React framework
- **CrewAI** for multi-agent orchestration
- **LangChain** team for LangGraph
- **Chroma** team for the vector database
- **Google** for Gemini AI and Cloud services

---

## 📊 System Status

| Component | Status | Version |
|-----------|--------|---------|
| Backend | ✅ Production Ready | 2.0.0 |
| Frontend | ✅ Production Ready | 2.0.0 |
| CrewAI | ✅ Integrated | 0.28.8 |
| LangGraph | ✅ Integrated | 0.0.20 |
| ChromaDB | ✅ Operational | 0.4.24 |
| Gemini AI | ✅ Configured | 1.5 Pro |
| Docker | ✅ Ready | Latest |

---

## 🚀 What's Next?

1. **Start the system**: `docker-compose up -d`
2. **Open dashboard**: http://localhost:3000
3. **Process your first document**
4. **Review generated content**
5. **Enjoy automated content creation!**

---

**Built with ❤️ for intelligent educational content creation**

*Last Updated: October 8, 2025 | Version 2.0.0 - Enhanced Edition*

---

**Ready to transform your educational content creation? Let's get started!** 🚀🎓✨
