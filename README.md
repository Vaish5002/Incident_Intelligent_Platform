# SmartOps AI - Incident Intelligence Platform

## 🎯 Project Overview

**SmartOps AI** is an intelligent incident management platform that automatically analyzes production incidents, identifies root causes, and generates comprehensive RCA reports using AI.

### The Problem
After production incidents, engineers spend 1-2 hours:
- Checking logs
- Reviewing recent commits  
- Finding root cause
- Writing RCA manually
- Suggesting fixes

### The Solution
Automate the entire process with AI-powered analysis.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SmartOps AI Platform                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Project 2: Chaos Demo                                  │
│  (Member 2)                                              │
│  └─→ Generates Real Failures                            │
│      └─→ Real Runtime Logs                              │
│                                                           │
│  ┌───────────────────────────────────────────┐          │
│  │                                             │          │
│  │  Project 1: SmartOps AI (Main Platform)   │          │
│  │                                             │          │
│  │  ┌─────────────────────────────────────┐  │          │
│  │  │  Member 1: Investigation Backend    │  │          │
│  │  │  • GitHub Agent                     │  │          │
│  │  │  • Log Agent                        │  │          │
│  │  │  • Incident Agent                   │  │          │
│  │  │  • Investigation Agent              │  │          │
│  │  └─────────────────┬───────────────────┘  │          │
│  │                    │                        │          │
│  │  ┌─────────────────▼───────────────────┐  │          │
│  │  │  Member 3: AI & RCA Engine    ✅    │  │          │
│  │  │  • Gemini Integration         ✅    │  │          │
│  │  │  • RAG System                 🔄    │  │          │
│  │  │  • RCA Generation             ✅    │  │          │
│  │  │  • PDF Reports                🔄    │  │          │
│  │  └─────────────────┬───────────────────┘  │          │
│  │                    │                        │          │
│  │  ┌─────────────────▼───────────────────┐  │          │
│  │  │  Member 4: Frontend & Visualization │  │          │
│  │  │  • Dashboard                        │  │          │
│  │  │  • Timeline UI                      │  │          │
│  │  │  • Knowledge Graph                  │  │          │
│  │  │  • Analytics                        │  │          │
│  │  └─────────────────────────────────────┘  │          │
│  │                                             │          │
│  └─────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

## 👥 Team Responsibilities

### Member 1 - Core Investigation Backend (Done by teammate)
- GitHub Agent (fetch commits, analyze changes)
- Log Agent (fetch logs from Chaos Platform)
- Incident Classification
- Timeline Generation
- **Status:** Being developed by teammate

### Member 2 - Chaos Demo Platform
- Real failure injection (DB timeout, memory leak, etc.)
- Runtime log generation
- Failure APIs
- **Status:** To be developed

### Member 3 - AI & RCA Engine (YOU - Current) ✅
- **Module 1: Gemini Integration** ✅ **COMPLETE**
  - RCA generation
  - Recommendations
  - Prevention strategies
- Module 2: RAG System 🔄 NEXT
- Module 3: Embeddings & Vector Search 🔄
- Module 4: PDF Generation 🔄
- Module 5: AI Copilot 🔄

### Member 4 - Frontend & Visualization (Done by teammate)
- Dashboard
- Timeline UI
- Knowledge Graph
- Analytics
- **Status:** Being developed by teammate

## 📁 Current Project Structure

```
Incident_Intelligent_Platform/
├── backend/                    # Member 3 - AI Engine (YOU)
│   ├── ai/
│   │   ├── config.py          # Configuration
│   │   ├── gemini_service.py  # Gemini AI service ✅
│   │   └── prompts.py         # Prompt templates ✅
│   ├── api/
│   │   └── rca_routes.py      # API routes ✅
│   ├── schemas/
│   │   └── rca.py             # Pydantic schemas ✅
│   ├── main.py                # FastAPI app ✅
│   ├── requirements.txt       # Dependencies ✅
│   ├── test_gemini.py         # Test script ✅
│   └── README.md              # Documentation ✅
├── QUICKSTART.md              # Quick start guide ✅
└── README.md                  # This file ✅
```

## ✅ Module 1: Gemini Integration (COMPLETE)

### What's Built:
- ✅ Google Gemini AI integration
- ✅ Comprehensive RCA generation
- ✅ Quick RCA for fast triage
- ✅ Recommendation generation
- ✅ Prevention strategy generation
- ✅ REST API with 4 endpoints
- ✅ Complete documentation
- ✅ Test scripts

### API Endpoints:
- `POST /api/generate-rca` - Generate comprehensive RCA
- `POST /api/quick-rca` - Quick RCA analysis
- `POST /api/recommendations` - Generate recommendations
- `GET /api/health` - Health check

### How to Use:
See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions.

Quick test:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Add GEMINI_API_KEY to .env
python test_gemini.py
python -m backend.main
```

Visit: http://localhost:8002/docs

## 🔄 Next: Module 2 - RAG System

**Goal:** Retrieve similar past incidents to learn from history.

**Features:**
- Incident embedding generation
- Vector similarity search
- Historical incident database
- Similar incident retrieval API

**Why it matters:**
- Learn from past incidents
- Identify recurring patterns
- Suggest proven solutions
- Prevent future occurrences

## 🚀 Getting Started (Member 3)

### Prerequisites
- Python 3.10+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Quick Start
```bash
# 1. Setup
cd backend
python -m venv venv
venv\Scripts\activate

# 2. Install
pip install -r requirements.txt

# 3. Configure
copy .env.example .env
# Edit .env, add GEMINI_API_KEY

# 4. Test
python test_gemini.py

# 5. Run
python -m backend.main
```

### Verify
- Test script passes: ✅
- Server starts: http://localhost:8002 ✅
- API docs accessible: http://localhost:8002/docs ✅
- Can generate RCA: ✅

## 🔗 Integration Status

| Integration | Status | Notes |
|-------------|--------|-------|
| Member 1 → Member 3 | 🔄 Ready | Waiting for Member 1's APIs |
| Member 3 → Member 4 | ✅ Ready | APIs documented and ready |
| Member 2 → Member 3 | 🔄 Pending | Will integrate later |

## 📊 Development Progress

### Member 3 Progress:
- [x] Project setup
- [x] Module 1: Gemini Integration
  - [x] Gemini service
  - [x] Prompt engineering
  - [x] RCA generation API
  - [x] Recommendations API
  - [x] Testing
  - [x] Documentation
- [ ] Module 2: RAG System (NEXT)
- [ ] Module 3: Embeddings
- [ ] Module 4: PDF Generation
- [ ] Module 5: AI Copilot

**Current Status:** Module 1 Complete ✅ (25% of Member 3's work)

## 📝 Next Steps

### For You (Member 3):
1. ✅ Complete Module 1 - Gemini Integration
2. 🔄 Start Module 2 - RAG System
3. 🔄 Build embedding service
4. 🔄 Create vector search
5. 🔄 Add PDF generation
6. 🔄 Build AI Copilot

### For Team Integration:
1. Wait for Member 1's investigation backend
2. Test end-to-end integration
3. Connect with Member 4's frontend
4. Deploy all services

## 🆘 Troubleshooting

### Common Issues:
- **GEMINI_API_KEY not set:** Check `.env` file
- **Module not found:** Activate virtual environment
- **Port in use:** Change `API_PORT` in `.env`
- **API key invalid:** Get new key from Google AI Studio

### Getting Help:
- Check `backend/README.md` for detailed docs
- Check `QUICKSTART.md` for setup guide
- Review API docs at `/docs` endpoint
- Check test script: `python test_gemini.py`

## 📚 Documentation

- **QuickStart:** [QUICKSTART.md](./QUICKSTART.md)
- **Backend Docs:** [backend/README.md](./backend/README.md)
- **API Docs:** http://localhost:8002/docs (when running)

## 🎯 Project Goal Reminder

**End Goal:**
User describes incident → SmartOps AI automatically:
1. Analyzes GitHub commits ✅ (Member 1)
2. Fetches runtime logs ✅ (Member 1 + Member 2)
3. Classifies incident ✅ (Member 1)
4. Generates RCA ✅ (Member 3 - Module 1 ✅)
5. Suggests recommendations ✅ (Member 3 - Module 1 ✅)
6. Shows similar past incidents 🔄 (Member 3 - Module 2)
7. Creates PDF report 🔄 (Member 3 - Module 4)
8. Displays in dashboard 🔄 (Member 4)

**Time saved:** From 1-2 hours to 2-3 minutes! 🚀

## 🎉 Achievements

- [x] Module 1: Gemini Integration ✅
- [x] Working RCA generation
- [x] REST API ready
- [x] Full documentation
- [x] Test coverage

**Next Milestone:** Module 2 - RAG System 🎯

---

**Member 3 - AI & RCA Engine**  
Module 1 Complete ✅ | Ready for Module 2 🚀
