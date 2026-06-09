# 🚀 QuickStart Guide - Member 3 (AI & RCA Engine)

## Module 1: Gemini Integration ✅

### ⚡ 5-Minute Setup

#### Step 1: Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

#### Step 2: Setup Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure
```bash
# Copy example env
copy .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_key_here
```

#### Step 4: Test It
```bash
# Run test script
python test_gemini.py
```

You should see:
```
✅ API Key configured
✅ Model: gemini-1.5-flash
✅ Gemini service initialized
✅ Quick RCA Generated
✅ Comprehensive RCA Generated
✅ All tests passed!
```

#### Step 5: Start Server
```bash
python -m backend.main
```

Server starts at: http://localhost:8002

#### Step 6: Test API
Open: http://localhost:8002/docs

Try this request:
```json
POST /api/generate-rca
{
  "incident": "Users cannot complete payments after deployment",
  "logs": "Database timeout, Pool exhausted",
  "timeline": "Deployment -> Config change -> Failure",
  "severity": "critical",
  "affected_service": "payment",
  "risk_score": 91.0
}
```

## 🎯 What You Built

✅ **Gemini Service** - AI-powered RCA generation  
✅ **REST API** - 4 endpoints for RCA, recommendations, etc.  
✅ **Prompt Engineering** - Optimized prompts for incident analysis  
✅ **Error Handling** - Robust error handling and logging  
✅ **Documentation** - Complete API docs at /docs  

## 🔗 Integration Points

### Input (from Member 1)
```python
# Member 1 sends investigation data
{
  "incident": "...",
  "github_analysis": {...},
  "log_analysis": {...},
  "timeline": {...}
}
```

### Output (to Member 4)
```python
# Member 3 returns RCA
{
  "rca_text": "## Root Cause Analysis\n\n...",
  "model_used": "gemini-1.5-flash",
  "success": true
}
```

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate-rca` | POST | Generate comprehensive RCA |
| `/api/quick-rca` | POST | Quick RCA for fast triage |
| `/api/recommendations` | POST | Generate recommendations |
| `/api/health` | GET | Health check |

## 🧪 Quick Test with cURL

```bash
# Test RCA generation
curl -X POST http://localhost:8002/api/generate-rca \
  -H "Content-Type: application/json" \
  -d "{\"incident\":\"Payment failures\",\"logs\":\"Database timeout\",\"timeline\":\"Deploy->Error\",\"severity\":\"critical\"}"
```

## 📚 Next Steps

1. ✅ **Module 1 Complete** - Gemini Integration
2. 🔄 **Module 2 Next** - RAG System (Similar incidents)
3. 🔄 **Module 3** - Embeddings & Vector Search
4. 🔄 **Module 4** - PDF Generation
5. 🔄 **Module 5** - AI Copilot

## 🆘 Troubleshooting

### "GEMINI_API_KEY not set"
→ Copy `.env.example` to `.env` and add your key

### "Module not found"
→ Make sure you're in the `backend/` directory

### "Port 8002 already in use"
→ Change `API_PORT` in `.env`

### "API key invalid"
→ Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 💡 Tips

- Use `gemini-1.5-flash` for development (fast, cheap)
- Use `gemini-1.5-pro` for production (more accurate)
- Adjust `TEMPERATURE` in `.env` (0.7 = balanced)
- Check `/docs` for interactive API testing

## ✅ Success Checklist

- [ ] Gemini API key obtained
- [ ] Dependencies installed
- [ ] Test script passes
- [ ] Server starts successfully
- [ ] Can generate RCA via API
- [ ] Documentation accessible at /docs

---

**🎉 Congratulations!** Module 1 is complete. Ready for Module 2?
