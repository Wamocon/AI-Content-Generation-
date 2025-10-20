# 🚀 FIAE AI Content Factory - Quick Start Guide

## ✅ System is Ready!

Everything has been fixed and optimized for **professional-grade automated content generation**.

---

## 📋 What You Get

### Input: `.docx` files from Google Drive
### Output: 4 Professional Documents per file

1. **📄 Use Cases (DOCX)** - 5-10 detailed IT scenarios (1-2 pages each)
2. **📝 Quiz (DOCX)** - 30-50 comprehensive questions with explanations
3. **🎓 Trainer Script (DOCX)** - Complete detailed presentation script
4. **📊 PowerPoint (PPTX)** - 40-60+ professional slides with speaker notes

---

## 🎯 Quick Start (2 Steps)

### Step 1: Start the System

**Option A: Docker (Recommended)**
```powershell
.\start_docker_system.ps1
```

**Option B: Native Python**
```powershell
.\start_system.ps1
```

### Step 2: Access the Application

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🤖 Run Automation

### From UI (Easiest)
1. Open http://localhost:3000
2. Click "Start Google Drive Processing"
3. Monitor progress in real-time

### From Command Line
```powershell
python automation_engine.py
```

---

## 📊 What Happens

1. **Discovery:** System finds all `.docx` files in your Google Drive source folder
2. **Processing:** Each document is processed with **FULL CONTENT** (no truncation!)
3. **AI Generation:** Creates 4 high-quality documents using latest Gemini model
4. **Upload:** Saves to Google Drive review folder in organized folders
5. **Notification:** Real-time progress via WebSocket

---

## ✨ Key Improvements

### Quality Fixes
✅ **Latest Gemini Model:** `gemini-2.0-flash-thinking-exp-1219`
✅ **Full Document Content:** No more 800-character truncation!
✅ **Proper Formats:** DOCX and PPTX files, not markdown
✅ **Detailed Prompts:** Professional, comprehensive content
✅ **Unlimited Output:** No artificial limits on slides/pages

### Document Quality
✅ **Use Cases:** 5-10 detailed scenarios with complete solutions
✅ **Quiz:** 30-50 questions covering 100% of topics
✅ **Trainer Script:** Complete speech text for every slide
✅ **PowerPoint:** 40-60+ slides with full topic coverage

---

## 🔧 Management Commands

### View Logs
```powershell
# All services
.\docker_logs.ps1

# Specific service
.\docker_logs.ps1 backend
.\docker_logs.ps1 frontend
```

### Stop System
```powershell
.\stop_docker_system.ps1
```

### Restart After Changes
```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 📁 Output Location

### Google Drive Structure
```
Review Folder/
├── FIAE_Production_Document1_20251013_100530/
│   ├── Anwendungsfälle_Document1.docx
│   ├── Quiz_Document1.docx
│   ├── Trainer-Skript_Document1.docx
│   └── Präsentation_Document1.pptx
├── FIAE_Production_Document2_20251013_100645/
│   ├── Anwendungsfälle_Document2.docx
│   ├── Quiz_Document2.docx
│   ├── Trainer-Skript_Document2.docx
│   └── Präsentation_Document2.pptx
...
```

---

## ⚙️ Environment Configuration

Your `.env` file should have:
```env
# Required
GEMINI_API_KEY=your-actual-api-key
GOOGLE_DRIVE_FOLDER_ID=your-source-folder-id
GOOGLE_DRIVE_REVIEW_FOLDER_ID=your-review-folder-id

# Automatically configured
GEMINI_MODEL_NAME=gemini-2.0-flash-thinking-exp-1219
```

---

## 🐛 Troubleshooting

### Issue: Poor quality results
**Solution:** Check that:
- `.env` has valid GEMINI_API_KEY
- Full document content is being used (check logs)
- No API quota limits reached

### Issue: No PPTX files
**Solution:**
```powershell
# Reinstall python-pptx
pip install python-pptx==0.6.23

# Or rebuild Docker
docker compose build --no-cache backend
```

### Issue: Frontend can't connect to backend
**Solution:** Check CORS settings in `docker-compose.yml`:
```yaml
environment:
  - ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 📚 Additional Resources

- **Complete Fixes:** `SYSTEM_FIXES_COMPLETE.md`
- **Docker Guide:** `DOCKER_DEPLOYMENT.md`
- **Full README:** `README.md`

---

## ✅ Verification Checklist

Before running automation:
- [ ] Docker containers running (or native services started)
- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Frontend accessible: http://localhost:3000
- [ ] `.env` file configured with valid credentials
- [ ] Google Drive folders accessible

After running automation:
- [ ] 4 documents created per source file
- [ ] Use Cases DOCX (5-10 scenarios, detailed)
- [ ] Quiz DOCX (30-50 questions, comprehensive)
- [ ] Trainer Script DOCX (complete script)
- [ ] PowerPoint PPTX (40-60+ slides)
- [ ] All files in Google Drive review folder
- [ ] Professional quality, proper formatting

---

## 🎉 You're All Set!

Your FIAE AI Content Factory is now a **production-ready automated content generation system**!

1. Start the system
2. Click "Start Google Drive Processing" in the UI
3. Watch as it generates professional documents automatically
4. Find your 4-document sets in Google Drive

**Quality:** ⭐⭐⭐⭐⭐ Professional Grade
**Status:** ✅ Ready to Use

---

**Need Help?** Check the logs or review `SYSTEM_FIXES_COMPLETE.md` for detailed information.

