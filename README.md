# FIAE AI Content Factory# FIAE AI Content Factory



**AI-Powered Use Case Generation System****AI-Powered Use Case Generation System**



[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![Status](https://img.shields.io/badge/status-production-green.svg)]()[![Status](https://img.shields.io/badge/status-production-green.svg)]()



---## 🎯 Overview



## 🎯 OverviewAutomated generation of high-quality German use cases (Anwendungsfälle) from source documents using AI-powered analysis and intelligent content generation.



Automated generation of high-quality German use cases (Anwendungsfälle) from source documents using AI-powered analysis and intelligent content generation.### Key Features



### Key Features- 🧠 **AI-Powered Analysis**: Intelligent document understanding with Google Gemini

- 📊 **Dynamic Generation**: Adapts to document size (3-40+ use cases)

- 🧠 **AI-Powered Analysis** - Intelligent document understanding with Google Gemini- ✅ **Quality Validation**: 6-point scoring system (0-100)

- 📊 **Dynamic Generation** - Adapts to document size (3-40+ use cases)- 📁 **Google Drive Integration**: Seamless upload/download

- ✅ **Quality Validation** - 6-point scoring system (0-100)- 🎯 **Agentic Architecture**: 3 AI agents working autonomously

- 📁 **Google Drive Integration** - Seamless upload/download- 📄 **Professional Output**: Formatted Word documents in German

- 🎯 **Agentic Architecture** - 3 AI agents working autonomously

- 📄 **Professional Output** - Formatted Word documents in German## ⚡ Quick Start (3 Commands)



---```powershell

# 1. Start Docker containers

## 🚀 Quick Startdocker-compose up -d



### Prerequisites# 2. Open Dashboard

# Visit: http://localhost:3000

- Python 3.11+

- Google Cloud credentials# 3. Process Documents

- Gemini API key# Click "Processing" → "Start Batch Processing"

- Virtual environment```



### Installation & Run**Access Points:**

- **Dashboard**: http://localhost:3000

1. **Navigate to project**- **Backend API**: http://localhost:8000

- **API Docs**: http://localhost:8000/docs

   ```powershell- **WebSocket**: ws://localhost:8000/ws

   cd "d:\FIAE Agents with RAG"

   ```---



2. **Activate environment**## 🏗️ Architecture



   ```powershell```

   .\.venv\Scripts\Activate.ps1┌─────────────────┐

   ```│  Google Drive   │  Source Documents (DOCX)

│  Source Folder  │

3. **Configure .env**└────────┬────────┘

         │

   ```bash         ↓

   GEMINI_API_KEY=your_key┌────────────────────────────────────────────────────────────┐

   GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=your_folder_id│              FIAE AI CONTENT FACTORY                       │

   GOOGLE_DRIVE_REVIEW_FOLDER_ID=your_folder_id│                                                            │

   ```│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐│

│  │   Frontend   │  │   Backend    │  │  AI Services    ││

4. **Run automation**│  │   Next.js 14 │◄─┤   FastAPI    │◄─┤  Multi-Agent    ││

│  │              │  │              │  │  Orchestration  ││

   ```powershell│  │ • Dashboard  │  │ • REST API   │  │                 ││

   python automation_phase1_content.py│  │ • Real-time  │  │ • WebSocket  │  │ • Gemini 1.5    ││

   ```│  │ • Monitoring │  │ • Automation │  │ • CrewAI (6)    ││

│  │              │  │              │  │ • LangGraph     ││

### Expected Output│  │              │  │              │  │ • ChromaDB RAG  ││

│  └──────────────┘  └──────────────┘  └─────────────────┘│

```│                                                            │

🚀 PHASE 1: ANWENDUNGSFÄLLE-GENERIERUNG│  Processing Pipeline (5 Phases):                         │

📚 5 Dokumente gefunden│  1. Content Extraction (text, images, tables)            │

[1/5] VERARBEITE: document1.docx│  2. Depth Analysis (calculate n-number requirements)     │

   🧠 Analysiere Dokument... (10 Anwendungsfälle empfohlen)│  3. RAG Enhancement (vector storage & retrieval)         │

   🤖 Generiere Anwendungsfälle...│  4. Content Generation (6 specialized AI agents)         │

   🔍 Qualität: 92/100 (EXCELLENT)│  5. Quality Assurance (validation & completeness)        │

   ✅ ERFOLG!│                                                            │

🎉 VERARBEITUNG ABGESCHLOSSEN└────────────────────────────────────────────────────────────┘

```         │

         ↓

---┌────────────────────────────────────────────────────────────┐

│                    Generated Content                       │

## 📦 System Architecture│  (Saved to Google Drive Review Folder)                    │

│                                                            │

### Agentic AI System│  ✓ PowerPoint (n slides)                                 │

│  ✓ Google Slides (interactive)                           │

The system uses **3 autonomous AI agents**:│  ✓ IT Use Cases (n pages with solutions)                 │

│  ✓ Quiz (n questions with answers)                       │

**🧠 Agent 1: Document Analyzer**│  ✓ Trainer Script (n pages)                              │

- Identifies topics and complexity│  ✓ Knowledge Analysis (backend)                          │

- Determines optimal use case count└────────────────────────────────────────────────────────────┘

- Uses: Gemini AI```



**🤖 Agent 2: Use Case Generator**---

- Generates detailed use cases in batches

- 100% topic coverage## 🚀 Features

- Content in German (5 sections per use case)

### **Content Generation**

**✅ Agent 3: Quality Validator**- **Dynamic Sizing**: Automatic calculation of slides/pages/questions based on source content

- 6-point quality check- **100% Coverage**: Every topic from source document included

- Scores 0-100 with grades- **Multi-Format**: PowerPoint, Google Slides, DOCX, text files

- Ensures professional standards- **Professional Quality**: German language, educational standard

- **Image Placeholders**: Detailed descriptions for every visual element

### Output Format

### **AI Orchestration**

Each generated Word document contains:- **LangGraph**: 5-phase workflow with state management

- **Title page** with metadata- **CrewAI**: 6 specialized agents:

- **Information table** (source, count, quality, date)  - Content Analyst (knowledge extraction)

- **Use cases** with 5 sections each:  - Presentation Creator (slides generation)

  - Theoretischer Hintergrund (Theory)  - Use Case Developer (IT scenarios)

  - Praxis-Szenario (Scenario)  - Quiz Master (assessment creation)

  - Aufgaben für Lernende (Tasks)  - Trainer Writer (scripts)

  - Musterlösung (Solution)  - Quality Assurance (validation)

  - Erwartete Ergebnisse (Expected Results)- **Gemini 1.5 Pro**: Optimized configuration (32K tokens)

- **Professional formatting** (headings, bullets, page breaks)- **RAG Enhancement**: ChromaDB vector database



---### **IT Industry Focus**

- **Practical Scenarios**: Real office environments

## 📁 Project Structure- **Task-Based**: Step-by-step instructions

- **Areas**: Project Management, Development, Testing, Infrastructure

```- **Solutions Included**: Complete answer keys

d:\FIAE Agents with RAG\

├── automation_phase1_content.py    ⭐ MAIN FILE### **Production Ready**

├── app/- **Docker**: Containerized deployment

│   ├── config.py- **Monitoring**: Real-time health checks

│   ├── models.py- **WebSocket**: Live progress updates

│   └── services/                   ⭐ ACTIVE SERVICES- **Error Handling**: Graceful fallbacks

│       ├── google_services.py- **Security**: OAuth2 & service account support

│       ├── intelligent_gemini_service.py

│       ├── document_analyzer.py---

│       └── gemini_ai_service.py

├── archived_phase2_components/     (Phase 2 - restorable)## 📊 Content Generation Examples

├── credentials/                    (Google API)

├── chroma_db/                      (For future use)### **Input: 5000-word Document about "Cloud Computing"**

├── .env                           ⭐ Configuration

├── requirements.txt**Generated Output:**

└── DOCUMENTATION.md               ⭐ Complete docs

```| Content Type | Quantity | Details |

|--------------|----------|---------|

---| **PowerPoint Slides** | 33 slides | Title, agenda, theory (simple), concepts (professional), examples, summary |

| **Google Slides** | 33 slides | Same structure + interactive elements & animations |

## 📊 Performance| **IT Use Cases** | 12 pages | 4 scenarios × 3 pages each with solutions |

| **Quiz Questions** | 50 questions | 20 easy + 20 medium + 10 hard with explanations |

| Document Size | Use Cases | Processing Time || **Trainer Script** | 33 pages | One page per slide with timing & interaction points |

|--------------|-----------|-----------------|| **Knowledge Analysis** | 1 document | Backend processing metadata |

| 1,000 words  | 3         | ~6 minutes      |

| 3,000 words  | 5         | ~10 minutes     |**Total Generated**: ~150 pages of professional educational material

| 6,000 words  | 10        | ~16 minutes     |

| 12,000 words | 20        | ~31 minutes     |**Processing Time**: 60-120 seconds



### Quality Distribution---

- **EXCELLENT (90-100):** 60%

- **GOOD (75-89):** 30%## 🔧 Installation & Setup

- **ACCEPTABLE (60-74):** 8%

- **NEEDS_IMPROVEMENT (<60):** 2%### **Prerequisites**

- Docker Desktop installed and running

---- Git (for cloning)

- Google Cloud credentials (optional, for Google Drive integration)

## 🔧 Configuration- Gemini API key (for AI content generation)



Key environment variables in `.env`:### **Method 1: Docker (Recommended)**



```env```powershell

# Required   ```powershell

GEMINI_API_KEY=your_gemini_api_key   cd "d:\FIAE Agents with RAG"

GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=source_folder_id   ```

GOOGLE_DRIVE_REVIEW_FOLDER_ID=review_folder_id

GOOGLE_APPLICATION_CREDENTIALS=credentials/file.json2. **Activate environment**



# Optional   ```powershell

LOG_LEVEL=INFO   .\.venv\Scripts\Activate.ps1

```   ```



---3. **Configure .env**



## 📖 Documentation   ```bash

   # Add to .env file:

**Complete documentation:** `DOCUMENTATION.md`   GEMINI_API_KEY=your_key

   GOOGLE_DRIVE_CONTENT_SOURCE_FOLDER_ID=your_folder_id

Includes:   GOOGLE_DRIVE_REVIEW_FOLDER_ID=your_folder_id

- Detailed architecture explanation   ```

- API reference

- Configuration guide4. **Run automation**

- Troubleshooting

- Archived components information   ```powershell

   python automation_phase1_content.py

---   ```



## 🗂️ Archived Components### Expected Output



Components for Phase 2 (presentations, quizzes) are archived in `archived_phase2_components/`:```

- 7 unused services🚀 PHASE 1: ANWENDUNGSFÄLLE-GENERIERUNG

- FastAPI web server📚 5 Dokumente gefunden

- Docker configuration[1/5] VERARBEITE: document1.docx

- Old automation files   🧠 Analysiere Dokument... (10 Anwendungsfälle empfohlen)

   🤖 Generiere Anwendungsfälle...

See `archived_phase2_components/README.md` for restoration instructions.   🔍 Qualität: 92/100 (EXCELLENT)

   ✅ ERFOLG!

---🎉 VERARBEITUNG ABGESCHLOSSEN

```

## 🛠️ Troubleshooting

# 2. Configure environment

**Import errors:**# Create .env file in root directory

```powershellcopy env.example .env

pip install -r requirements.txt# Edit .env with your settings

```

# 3. Build and start

**Google Drive connection failed:**docker-compose build

- Check `.env` credentialsdocker-compose up -d

- Verify folder IDs

- Ensure `credentials/` has JSON file# 4. Check status

docker ps

**Gemini API errors:**# Should show: fiae-backend (healthy), fiae-frontend (healthy)

- Verify `GEMINI_API_KEY` in `.env`

- Check API quota/rate limits# 5. Access dashboard

- System has automatic retry (3 attempts)# Open: http://localhost:3000

```

---

### **Method 2: Manual Setup**

## 📌 Quick Reference

```powershell

**Main command:**# Backend

```powershellpip install -r requirements.txt

python automation_phase1_content.pypython -m uvicorn app.main:app --host 0.0.0.0 --port 8000

```

# Frontend (new terminal)

**Key files:**cd frontend

- Main: `automation_phase1_content.py`npm install

- Config: `.env`, `app/config.py`npm run dev

- Docs: `DOCUMENTATION.md````



**Google Drive folders:**---

- Source: `1YtN3_CftdJGgK9DFGLSMIky7PbYfFsX5`

- Review: `1fBJdZKHLR-5jxfwKj8RLG45rKyZU8cXb`## ⚙️ Configuration



---### **Required Environment Variables**



## ✅ System StatusCreate `.env` in root directory:



- **Status:** Production-ready ✅```bash

- **Version:** 2.0 (Phase 1)# Core Settings

- **Python:** 3.11.9ENVIRONMENT=production

- **Last Updated:** November 11, 2025API_HOST=0.0.0.0

API_PORT=8000

---LOG_LEVEL=INFO



**For complete documentation, see `DOCUMENTATION.md`**# Google Services (Optional - for Google Drive integration)

GOOGLE_CREDENTIALS_PATH=credentials/your-service-account.json
GOOGLE_DRIVE_FOLDER_ID=your_source_folder_id
GOOGLE_DRIVE_REVIEW_FOLDER_ID=your_review_folder_id
GOOGLE_SHEETS_ID=your_tracking_sheet_id

# AI Services (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
BACKEND_URL=http://backend:8000
WS_URL=ws://backend:8000/ws
```

---

## 📖 Usage Guide

### **Dashboard Features**

#### **Main Dashboard**
- System health status
- Active jobs counter
- Documents processed
- Service status panel
- Real-time updates

#### **Processing Page**
1. Click "Discover Documents" to scan Google Drive
2. Click "Start Batch Processing" to begin automation
3. Monitor real-time progress via WebSocket
4. Check results in Google Drive review folder

#### **Agents Page**
- View all 6 CrewAI agents
- Start individual agent workflows
- Monitor agent collaboration
- Track task completion

#### **RAG Page**
- Vector database status
- Document embedding count
- Process documents with RAG
- Reset knowledge base

#### **Monitoring Page**
- System metrics
- Performance graphs
- Active alerts
- Error tracking

---

## 📂 Project Structure

```
FIAE Agents with RAG/
├── app/                                # Backend FastAPI application
│   ├── main.py                         # Main API application (2205 lines)
│   ├── config.py                       # Settings management
│   ├── models.py                       # Pydantic data models
│   └── services/                       # AI & integration services
│       ├── rag_enhanced_processor.py   # RAG + Gemini processor (627 lines)
│       ├── crewai_orchestrator.py      # Multi-agent system (389 lines)
│       ├── langgraph_orchestrator.py   # Workflow management (365 lines)
│       ├── advanced_document_processor.py # Document extraction (285 lines)
│       ├── google_services.py          # Google Drive/Sheets (396 lines)
│       ├── gemini_ai_service.py        # Gemini AI service
│       ├── content_intelligence.py     # Content analysis
│       └── production_monitor.py       # System monitoring
│
├── frontend/                           # Next.js 14 application
│   ├── src/
│   │   ├── app/                        # App router pages
│   │   │   ├── page.tsx                # Main dashboard
│   │   │   ├── processing/            # Processing queue
│   │   │   ├── agents/                # Agent workflows
│   │   │   ├── rag/                   # RAG management
│   │   │   ├── monitoring/            # System monitoring
│   │   │   ├── analytics/             # Analytics
│   │   │   └── review/                # HITL review
│   │   ├── components/                # React components (20+)
│   │   ├── services/
│   │   │   ├── api-client.ts          # API service layer (450 lines)
│   │   │   └── websocket.ts           # WebSocket client
│   │   └── hooks/                     # Custom React hooks
│   │       ├── useApi.ts
│   │       └── useWebSocket.ts
│   └── package.json
│
├── automation_engine.py                # Main automation script (393 lines)
├── personal_google_drive_service.py    # OAuth2 personal account
├── credentials/                        # Google credentials
│   ├── README.md
│   └── wmc-automation-agents-*.json    # Service account
├── chroma_db/                          # Vector database storage
├── logs/                               # Application logs
├── docker-compose.yml                  # Production config
├── docker-compose.dev.yml              # Development config
├── Dockerfile.backend                  # Backend image
├── Dockerfile.frontend                 # Frontend image
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Python project config
├── .env.example                        # Environment template
├── build_and_start.ps1                 # Build automation script
└── README.md                           # This file
```

---

## 🎯 Content Generation Formula

| Content Type | Formula | Min | Max | Example (5000 words) |
|--------------|---------|-----|-----|----------------------|
| **PowerPoint Slides** | words ÷ 150 | 10 | 50 | 33 slides |
| **Google Slides** | Same as PPT | 10 | 50 | 33 slides |
| **Use Case Pages** | words ÷ 400 | 3 | 20 | 12 pages |
| **Quiz Questions** | words ÷ 100 | 10 | 50 | 50 questions |
| **Trainer Script** | 1 page/slide | 10 | 50 | 33 pages |

---

## 🤖 AI Processing Pipeline

### **Phase 1: Content Extraction**
- Full text extraction from DOCX
- Image extraction with metadata
- Table extraction with formatting
- Metadata collection

### **Phase 2: Depth Analysis**
- Word count calculation
- Topic density assessment
- Required output sizing (n-number)
- Content complexity evaluation

### **Phase 3: RAG Enhancement**
- Document chunking (1000 chars, 200 overlap)
- Embedding generation (Sentence Transformers)
- Vector storage (ChromaDB)
- Semantic search preparation

### **Phase 4: Content Generation**
- **CrewAI Multi-Agent Collaboration**:
  - Agent 1: Analyzes content, extracts knowledge
  - Agent 2: Creates PowerPoint & Google Slides
  - Agent 3: Develops IT use cases with solutions
  - Agent 4: Generates multi-difficulty quizzes
  - Agent 5: Writes trainer scripts
  - Agent 6: Validates quality & completeness

### **Phase 5: Quality Assurance**
- Completeness validation (100% coverage check)
- Content quality scoring
- Format verification
- Error detection

---

## 📱 API Endpoints

### **System Health**
- `GET /health` - Basic health check
- `GET /monitoring/health` - Detailed health metrics
- `GET /monitoring/metrics` - System performance metrics

### **Document Processing**
- `POST /process-document` - Process single document
- `POST /process-document-upload` - Upload & process
- `POST /process-comprehensive-batch` - Batch processing
- `POST /process-document-rag` - RAG-enhanced processing
- `POST /process-document-orchestrated` - LangGraph orchestration

### **Batch Operations**
- `GET /discover-documents` - Scan Google Drive folder
- `GET /batch-status` - Current batch status
- `POST /abort-automation/{job_id}` - Cancel running job

### **AI Services**
- `GET /crewai/status` - CrewAI agent status
- `POST /crewai/run-workflow` - Start agent workflow
- `GET /rag/status` - RAG system status
- `POST /rag/reset` - Reset knowledge base

### **Monitoring**
- `GET /production-monitor/status` - System status
- `GET /production-monitor/metrics` - Performance metrics
- `GET /production-monitor/alerts` - Active alerts

### **Real-time**
- `WS /ws` - WebSocket for live updates

**Full API Documentation**: http://localhost:8000/docs

---

## 🔍 Monitoring & Debugging

### **Health Checks**

```powershell
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Docker container status
docker ps

# View logs
docker logs fiae-backend
docker logs fiae-frontend
```

### **Common Issues & Solutions**

#### **Problem**: Containers won't start
```powershell
# Solution 1: Check if ports are available
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Solution 2: Restart Docker Desktop
# Close Docker Desktop → Restart

# Solution 3: Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### **Problem**: Frontend can't connect to backend
```bash
# Check backend is running
docker ps | grep fiae-backend

# Check environment variables
docker exec fiae-frontend env | grep NEXT_PUBLIC

# Verify in frontend/.env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

#### **Problem**: Content generation fails
```bash
# Check Gemini API key
docker exec fiae-backend env | grep GEMINI_API_KEY

# Check logs for errors
docker logs fiae-backend | grep -i error

# Verify API quota at Google Cloud Console
```

#### **Problem**: OAuth2 authentication fails
```bash
# Solution:
# 1. Delete token file
rm personal_google_token.pickle

# 2. Re-run authentication
python personal_google_drive_service.py

# 3. Complete browser authentication

# 4. Restart containers
docker-compose restart
```

---

## 🔒 Security

### **Credential Files (Protected)**

**DO NOT DELETE OR COMMIT:**
- `personal_credentials.json` - OAuth2 client credentials
- `personal_google_token.pickle` - OAuth2 access tokens
- `credentials/wmc-automation-agents-*.json` - Service account key

### **Environment Variables**
- Never commit `.env` files
- Use `.env.example` as template
- Rotate API keys regularly
- Use service accounts for automation

### **Best Practices**
- Enable 2FA on Google accounts
- Restrict service account permissions
- Use HTTPS in production
- Implement rate limiting
- Monitor API usage

---

## 📈 Performance

### **Expected Performance**
- **Small docs** (1000 words): ~45 seconds
- **Medium docs** (3000 words): ~75 seconds
- **Large docs** (5000+ words): ~120 seconds

### **Resource Requirements**
- **RAM**: 2-3 GB total (backend + frontend)
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
