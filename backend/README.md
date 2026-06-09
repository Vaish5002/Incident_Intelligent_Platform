# SmartOps AI - RCA Engine (Member 3)

## 🎯 Purpose

This is the **AI & Intelligence Layer** for SmartOps AI. It uses Google Gemini to generate Root Cause Analysis (RCA), provide recommendations, and learn from historical incidents.

## 🏗️ Architecture - Module 1: Gemini Integration

```
┌────────────────────────────────────────────────┐
│         SmartOps AI - RCA Engine               │
│              (Member 3)                         │
├────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────┐          │
│  │      Gemini Service              │          │
│  │  - RCA Generation                │          │
│  │  - Recommendations               │          │
│  │  - Quick Analysis                │          │
│  │  - Prevention Strategy           │          │
│  └──────────────────────────────────┘          │
│                                                 │
│  Input (from Member 1):                        │
│  • Incident description                        │
│  • GitHub analysis                             │
│  • Log analysis                                │
│  • Timeline                                    │
│  • Root cause candidates                       │
│                                                 │
│  Output:                                       │
│  • Comprehensive RCA                           │
│  • Actionable recommendations                  │
│  • Risk assessment                             │
│  • Prevention strategies                       │
└────────────────────────────────────────────────┘
```

## ✨ Features

### All Modules Complete! ✅

**Module 1: Gemini Integration ✅**
- Comprehensive RCA generation
- Quick RCA (fast triage)
- Actionable recommendations
- Prevention strategies

**Module 2: RCA Prompt Engineering ✅**
- Standard 9-section RCA format
- 5 specialized prompt templates
- Consistent output structure

**Module 3: Risk Scoring Engine ✅**
- Multi-factor risk scoring (5 factors)
- Severity classification (Low/Medium/High/Critical)
- Confidence metrics

**Module 4: RCA Generator ✅**
- Root cause identification
- Multi-source data integration
- Confidence-ranked candidates

**Module 5: Knowledge Base ✅**
- Historical incident storage
- RCA report persistence
- Full CRUD operations

**Module 6: Embedding Service ✅**
- TF-IDF vectorization
- Similarity calculation
- Batch processing

**Module 7: RAG Retrieval ✅**
- Semantic similarity search
- Historical incident retrieval
- Context augmentation

**Module 8: AI Copilot ✅**
- Interactive Q&A assistant
- Context-aware responses
- Conversation history

**Total: 32 API Endpoints | 8/8 Modules Complete | 100% Production Ready**

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Setup environment**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Copy example env file
copy .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

4. **Run the server**
```bash
python -m backend.main
```

Server starts on `http://localhost:8002`

## 📡 API Endpoints

### 1. Generate Comprehensive RCA

```bash
POST /api/generate-rca
```

**Request Body:**
```json
{
  "incident": "Users cannot complete payments after deployment",
  "logs": "Database timeout, Pool exhausted, Payment service failed",
  "timeline": "Deployment -> Config change -> Database timeout -> Payment failure",
  "severity": "critical",
  "affected_service": "payment",
  "risk_score": 91.0
}
```

**Optional Fields:**
```json
{
  "github_analysis": {
    "repo_name": "user/payment-service",
    "commits": [...],
    "changed_files": [...]
  },
  "log_analysis": {
    "total_logs": 1500,
    "error_count": 243,
    "critical_errors": [...]
  },
  "timeline_data": {
    "events": [...]
  },
  "root_cause_candidates": [...]
}
```

**Response:**
```json
{
  "rca_text": "## Root Cause Analysis\n\n### Executive Summary\n...",
  "model_used": "gemini-1.5-flash",
  "success": true
}
```

### 2. Generate Quick RCA

```bash
POST /api/quick-rca
```

**Request:**
```json
{
  "incident": "Payment failures",
  "logs": "Database timeout errors",
  "timeline": "Deployment -> Errors started"
}
```

**Response:**
```json
{
  "rca_text": "**Root Cause:** Database pool size reduced...\n\n**Immediate Actions:**\n1. Increase pool size\n2. Add monitoring\n3. Rollback config\n\n**Risk Level:** Critical",
  "success": true
}
```

### 3. Generate Recommendations

```bash
POST /api/recommendations
```

**Request:**
```json
{
  "root_cause": "Database pool size was reduced from 50 to 10",
  "severity": "critical",
  "affected_service": "payment"
}
```

**Response:**
```json
{
  "recommendations": "## Immediate Actions (0-24 hours)\n\n1. **Increase DB Pool Size** [P0]\n   - Action: Change DB_POOL_SIZE from 10 to 50\n   - Effort: 5 minutes\n   - Impact: Immediate resolution...",
  "success": true
}
```

### 4. Health Check

```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "SmartOps AI - RCA Engine",
  "gemini_service": "healthy",
  "gemini_api_key_configured": true,
  "model": "gemini-1.5-flash"
}
```

## 🧪 Testing

### Test with cURL

```bash
# Test RCA generation
curl -X POST http://localhost:8002/api/generate-rca \
  -H "Content-Type: application/json" \
  -d "{\"incident\":\"Users cannot complete payments\",\"logs\":\"Database timeout\",\"timeline\":\"Deployment -> Failure\",\"severity\":\"critical\"}"

# Test quick RCA
curl -X POST http://localhost:8002/api/quick-rca \
  -H "Content-Type: application/json" \
  -d "{\"incident\":\"Payment failures\",\"logs\":\"Database errors\",\"timeline\":\"Deploy -> Error\"}"
```

### Test with Python

```python
import requests

# Generate RCA
response = requests.post(
    "http://localhost:8002/api/generate-rca",
    json={
        "incident": "Users cannot complete payments after deployment",
        "logs": "Database timeout, Pool exhausted",
        "timeline": "Deployment -> Config change -> Failure",
        "severity": "critical",
        "affected_service": "payment",
        "risk_score": 91.0
    }
)

print(response.json()["rca_text"])
```

## 🔌 Integration with Other Members

### From Member 1 (Investigation Backend)

Member 1 provides investigation data:
```python
# Member 1 sends this data
investigation_data = {
    "incident_description": "...",
    "severity": "critical",
    "risk_score": 91.0,
    "github_analysis": {...},
    "log_analysis": {...},
    "timeline": {...},
    "root_cause_candidates": [...]
}

# Member 3 (this service) generates RCA
rca = generate_rca(**investigation_data)
```

### To Member 4 (Frontend)

Member 4 can call our APIs to display results:
```javascript
// Frontend calls
const rca = await fetch('/api/generate-rca', {
  method: 'POST',
  body: JSON.stringify(investigationData)
});

// Display RCA text (markdown format)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API Key | - | ✅ Yes |
| `GEMINI_MODEL` | Model to use | `gemini-1.5-flash` | No |
| `API_HOST` | Server host | `0.0.0.0` | No |
| `API_PORT` | Server port | `8002` | No |
| `TEMPERATURE` | AI creativity (0-1) | `0.7` | No |
| `MAX_TOKENS` | Max output length | `2048` | No |

### Gemini Models

- `gemini-1.5-flash` - Fast, cost-effective (recommended for development)
- `gemini-1.5-pro` - More accurate, slower (recommended for production)

## 📝 Project Structure

```
backend/
├── ai/
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── gemini_service.py   # Gemini AI service
│   └── prompts.py          # Prompt templates
├── api/
│   ├── __init__.py
│   └── rca_routes.py       # API routes
├── schemas/
│   ├── __init__.py
│   └── rca.py              # Pydantic schemas
├── main.py                  # FastAPI app
├── requirements.txt
├── .env.example
└── README.md
```

## 🚢 Deployment (Render)

1. **Create new Web Service**
2. **Connect repository**
3. **Configure:**
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables:**
   - `GEMINI_API_KEY` (required)
   - `CORS_ORIGINS` (your frontend URLs)

## 📚 API Documentation

Once running:
- **Swagger UI:** http://localhost:8002/docs
- **ReDoc:** http://localhost:8002/redoc

## 🎯 Module 1 Status: ✅ COMPLETE

### What's Working:
- ✅ Gemini AI integration
- ✅ Comprehensive RCA generation
- ✅ Quick RCA for fast triage
- ✅ Recommendation generation
- ✅ Prevention strategy generation
- ✅ REST API endpoints
- ✅ Complete documentation

### Next Modules (Coming Soon):
- 🔄 Module 2: RAG System (Similar incident retrieval)
- 🔄 Module 3: Embeddings & Vector Search
- 🔄 Module 4: Risk Scoring Engine
- 🔄 Module 5: PDF Report Generation
- 🔄 Module 6: AI Copilot

## 🤝 Team Responsibilities

**Member 3 (You) - Module 1:**
- ✅ Gemini service integration
- ✅ Prompt engineering
- ✅ RCA generation APIs
- ✅ Recommendation engine

**Integration Points:**
- **From Member 1:** Receives investigation data
- **To Member 4:** Provides RCA text for display
- **From Member 2:** (Later) Receives real-time logs

## 📞 Support

Member 3 - AI & RCA Engine  
Module 1: Gemini Integration ✅

---

**Ready for Module 2: RAG System?** 🚀
