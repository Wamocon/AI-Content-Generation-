# Archived Components

This folder contains **deprecated automation scripts and components** that are no longer used in the current system but are preserved for reference.

## 📦 What's Archived

### **Old Automation Scripts**

1. **`automation_phase1_content.py`** (888 lines)
   - **Purpose**: Original single comprehensive use case generation
   - **Status**: Superseded by DiTeLe system
   - **Replaced by**: `../automation_ditele.py`
   - **Why archived**: Stakeholder feedback (Nikolaj, Erwin, Waleri) required complete restructure to DiTeLe standard

2. **`automation_phase2_presentation.py`** (442 lines)
   - **Purpose**: Presentation generation (Trainer Script + PowerPoint)
   - **Status**: Phase 2 work (not actively used)
   - **Why archived**: Focus shifted to DiTeLe content generation (Phase 1 priority)

3. **`automation_engine.py`** (1749 lines)
   - **Purpose**: Comprehensive automation engine with WebSocket progress updates
   - **Status**: Full-featured but overly complex for current needs
   - **Why archived**: DiTeLe system is simpler and more focused

4. **`test_single_use_case.py`**
   - **Purpose**: Test script for old single use case system
   - **Status**: Tests functions from `automation_phase1_content.py`
   - **Why archived**: No longer applicable to DiTeLe system

### **Phase 2 Components** (`phase2_components/`)

Complete Phase 2 system including:
- FastAPI web server
- Docker configuration
- Advanced document processor
- RAG-enhanced processor
- CrewAI orchestrator
- LangGraph orchestrator
- Production monitoring
- Content intelligence services

**Status**: Fully functional but not needed for current DiTeLe workflow. Can be restored if needed.

---

## 🔄 Current Active System

**Main File**: `../automation_ditele.py`

**Purpose**: Generate educational scenarios following **DiTeLe standard structure**

**Key Features**:
- ✅ 6-section DiTeLe-compliant structure
- ✅ Multiple problem-solution pairs (one per topic)
- ✅ Expanded theory section (800+ words)
- ✅ Test mode (processes 2 docs first for quality review)
- ✅ Professional Word document generation
- ✅ Google Drive integration

---

## 🔧 Restoration Instructions

If you need to restore any archived component:

```powershell
# Restore old Phase 1 system
Move-Item "archived\automation_phase1_content.py" ".\"

# Restore Phase 2 system
Move-Item "archived\automation_phase2_presentation.py" ".\"

# Restore full engine
Move-Item "archived\automation_engine.py" ".\"

# Restore Phase 2 components (Docker, APIs, etc.)
Move-Item "archived\phase2_components" "archived_phase2_components"
```

---

## 📅 Archive Information

- **Archived Date**: November 18, 2025
- **Reason**: Codebase cleanup and consolidation
- **Decision**: Stakeholder requirements changed to DiTeLe standard
- **Status**: Preserved for reference, not actively maintained

---

## ⚠️ Important Notes

- **DO NOT DELETE** these files - they contain valuable reference code
- **DO NOT USE** these files directly - they are outdated
- **DO USE** the current `automation_ditele.py` for all content generation
- If you need features from archived code, port them to the current system

---

**For current system documentation, see: `../README.md`**
