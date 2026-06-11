# 📋 SmartOps AI - Requirements Verification Checklist

**Date:** June 9, 2026  
**Purpose:** Verify all modules match project requirements

---

## 🎯 Project Requirements Overview

### End-to-End Flow Required:
1. User inputs GitHub URL + Incident Description
2. **GitHub Agent** → Fetch commits, changed files, messages
3. **Log Agent** → Fetch runtime logs from Chaos Demo (Project 2)
4. **Incident Agent** → Determine severity, affected service, business impact
5. **Investigation Agent** → Correlate GitHub + Logs + Incident data
6. **RAG Agent** → Find similar historical incidents
7. **Gemini Agent** → Generate RCA report
8. **Risk Engine** → Calculate severity, risk score, confidence
9. **Dashboard** → Display results with knowledge graph
10. **AI Copilot** → Answer questions about incident
11. **PDF Generator** → Create downloadable report

---

## 👥 Member Responsibilities

### Member 1: Investigation Backend
- [ ] GitHub Agent (fetch commits, analyze changes)
- [ ] Log Agent (fetch logs from Project 2 Chaos Platform)
- [ ] Incident Agent (determine severity, affected service, impact)
- [ ] Investigation Engine (correlate all data, build timeline)
- [ ] Timeline APIs

### Member 2: Chaos Demo Platform (Separate Project)
- [ ] Failure injection (DB timeout, memory leak, CPU spike, etc.)
- [ ] Runtime log generation
- [ ] Logs APIs: GET /logs, GET /failures, GET /status
- [ ] Deploy to Render
- [ ] SQLite storage for logs

### Member 3: AI & RCA Engine (You)
- [ ] Gemini Integration (RCA generation using AI)
- [ ] RAG System (find similar historical incidents)
- [ ] Embeddings (TF-IDF or vector embeddings)
- [ ] Risk Engine (severity, risk score, confidence)
- [ ] RCA Generator (structured RCA format)
- [ ] AI Copilot (Q&A about incident)
- [ ] PDF Generator (downloadable RCA report)

### Member 4: Frontend Dashboard
- [ ] Dashboard (incident overview)
- [ ] Timeline UI (visual timeline of events)
- [ ] Knowledge Graph (visual correlation)
- [ ] Analytics (metrics and trends)
- [ ] Results Screen (display RCA)
- [ ] Monitoring (incident tracking)

---

## 📊 Module-by-Module Requirements Check

---

## ✅ MEMBER 1: Investigation Backend

### Module 1.1: GitHub Agent
**Required Functionality:**
- [ ] Accept GitHub repository URL as input
- [ ] Fetch recent commits (last 10-20 commits)
- [ ] Extract: commit hash, message, author, timestamp
- [ ] Extract changed files for each commit
- [ ] Detect config changes (e.g., DB_POOL_SIZE change)
- [ ] API endpoint to trigger GitHub analysis
- [ ] Return structured GitHub data

**Expected Output:**
```json
{
  "commits": [
    {
      "hash": "abc123",
      "message": "Update DB config",
      "author": "john@company.com",
      "timestamp": "2024-01-15T10:30:00Z",
      "changed_files": ["config/db.py"],
      "changes": {
        "config/db.py": "DB_POOL_SIZE: 50 → 10"
      }
    }
  ]
}
```

---

### Module 1.2: Log Agent
**Required Functionality:**
- [ ] Connect to Project 2 (Chaos Demo) logs API
- [ ] Fetch logs from: `GET /logs`
- [ ] Parse log entries (timestamp, level, message)
- [ ] Filter ERROR and CRITICAL logs
- [ ] Detect failure patterns (timeout, pool exhausted, etc.)
- [ ] API endpoint to fetch and analyze logs
- [ ] Return structured log data

**Expected Output:**
```json
{
  "logs": [
    {
      "timestamp": "2024-01-15T10:32:45Z",
      "level": "ERROR",
      "message": "Database Timeout",
      "service": "payment-service"
    },
    {
      "timestamp": "2024-01-15T10:32:46Z",
      "level": "ERROR",
      "message": "Connection pool exhausted"
    }
  ],
  "failure_type": "Database Timeout"
}
```

---

### Module 1.3: Incident Agent
**Required Functionality:**
- [ ] Accept incident description from user
- [ ] Classify incident type (payment, database, API, etc.)
- [ ] Determine affected service
- [ ] Assess business impact (high/medium/low)
- [ ] Determine initial severity
- [ ] API endpoint to analyze incident
- [ ] Return structured incident data

**Expected Output:**
```json
{
  "incident_type": "Payment Failure",
  "affected_service": "payment-service",
  "business_impact": "High",
  "initial_severity": "Critical",
  "user_impact": "Users unable to complete payments"
}
```

---

### Module 1.4: Investigation Engine
**Required Functionality:**
- [ ] Receive data from: GitHub Agent + Log Agent + Incident Agent
- [ ] Correlate timeline: Deployment → Config Change → Error
- [ ] Build causal chain (what caused what)
- [ ] Identify correlation between commit and error
- [ ] Generate timeline of events
- [ ] API endpoint to trigger investigation
- [ ] Return correlation data

**Expected Output:**
```json
{
  "timeline": [
    {
      "time": "2024-01-15T10:00:00Z",
      "event": "Deployment",
      "details": "Commit abc123 deployed"
    },
    {
      "time": "2024-01-15T10:30:00Z",
      "event": "Config Change",
      "details": "DB_POOL_SIZE changed from 50 to 10"
    },
    {
      "time": "2024-01-15T10:32:45Z",
      "event": "Database Timeout",
      "details": "Connection pool exhausted"
    },
    {
      "time": "2024-01-15T10:33:00Z",
      "event": "Payment Failures",
      "details": "Users unable to complete payments"
    }
  ],
  "correlation": {
    "commit": "abc123",
    "change": "DB_POOL_SIZE: 50 → 10",
    "result": "Database Timeout → Payment Failures"
  }
}
```

---

## ✅ MEMBER 3: AI & RCA Engine (You)

### Module 3.1: Gemini Integration
**Required Functionality:**
- [ ] Integrate Google Gemini AI
- [ ] Accept investigation data as input
- [ ] Generate RCA with sections:
  - [ ] Executive Summary
  - [ ] Root Cause
  - [ ] Impact Analysis
  - [ ] Timeline
  - [ ] Recommendations
  - [ ] Prevention Plan
- [ ] API endpoint: POST /api/generate-rca
- [ ] Return structured RCA text

**Expected Output:**
```json
{
  "executive_summary": "...",
  "root_cause": "DB_POOL_SIZE reduced from 50 to 10...",
  "impact": "Users unable to complete payments...",
  "timeline": "...",
  "recommendations": ["Increase DB Pool Size", "Add monitoring"],
  "prevention": "Deployment validation pipeline"
}
```

**Current Status:** ✅ IMPLEMENTED

---

### Module 3.2: RAG System
**Required Functionality:**
- [ ] Store historical incidents in database
- [ ] Generate embeddings for incident descriptions
- [ ] Accept new incident description
- [ ] Search for similar past incidents
- [ ] Return top 3-5 similar incidents with similarity score
- [ ] API endpoint: POST /api/rag/find-similar
- [ ] Include previous solutions/fixes

**Expected Output:**
```json
{
  "similar_incidents": [
    {
      "incident_id": "INC-001",
      "description": "Payment failures due to DB connection",
      "similarity": 0.89,
      "root_cause": "Database pool exhaustion",
      "solution": "Increased pool size to 100",
      "occurred_at": "2023-12-10"
    }
  ]
}
```

**Current Status:** ✅ IMPLEMENTED

---

### Module 3.3: Risk Engine
**Required Functionality:**
- [ ] Accept incident data
- [ ] Calculate severity: Low/Medium/High/Critical
- [ ] Calculate risk score (0-100)
- [ ] Calculate confidence score (0-100)
- [ ] Consider factors:
  - [ ] Service criticality
  - [ ] User impact
  - [ ] Data loss potential
  - [ ] Recovery complexity
  - [ ] Downtime duration
- [ ] API endpoint: POST /api/risk-score
- [ ] Return risk assessment

**Expected Output:**
```json
{
  "severity": "Critical",
  "risk_score": 91,
  "confidence": 95,
  "factors": {
    "service_criticality": "High",
    "user_impact": "High",
    "data_loss": "None",
    "recovery_complexity": "Medium",
    "downtime": "15 minutes"
  }
}
```

**Current Status:** ✅ IMPLEMENTED

---

### Module 3.4: AI Copilot
**Required Functionality:**
- [ ] Accept questions from users
- [ ] Question types:
  - [ ] "Why did this happen?"
  - [ ] "Which commit caused this?"
  - [ ] "How can we prevent this?"
  - [ ] "What should we do next?"
- [ ] Use RCA context to answer
- [ ] Maintain conversation history
- [ ] API endpoint: POST /api/copilot/ask
- [ ] Return contextual answers

**Expected Output:**
```json
{
  "question": "Why did this happen?",
  "answer": "The incident occurred because DB_POOL_SIZE was reduced from 50 to 10 in commit abc123, causing connection pool exhaustion when traffic increased.",
  "confidence": 0.95
}
```

**Current Status:** ✅ IMPLEMENTED

---

### Module 3.5: PDF Generator
**Required Functionality:**
- [ ] Accept RCA data
- [ ] Generate PDF with:
  - [ ] Title page
  - [ ] Executive Summary
  - [ ] Timeline (formatted)
  - [ ] Root Cause (formatted)
  - [ ] Severity & Risk Score (visual)
  - [ ] Recommendations (bullet list)
  - [ ] Prevention Plan
- [ ] API endpoint: POST /api/pdf/generate-rca
- [ ] Return downloadable PDF file
- [ ] Professional formatting

**Expected Output:**
```
PDF file with:
- Header: "Root Cause Analysis Report"
- Incident ID, Date, Severity
- All sections formatted
- Tables, bullet points
- Color-coded severity
```

**Current Status:** ✅ IMPLEMENTED

---

## ✅ MEMBER 4: Frontend Dashboard

### Module 4.1: Dashboard
**Required Functionality:**
- [ ] Display incident overview
- [ ] Show active incidents count
- [ ] Display recent incidents list
- [ ] Quick actions (create incident, view reports)
- [ ] Summary statistics

**Current Status:** ✅ IMPLEMENTED (Dashboard.jsx)

---

### Module 4.2: Timeline UI
**Required Functionality:**
- [ ] Visual timeline of events
- [ ] Show: Deployment → Config → Error → Failure
- [ ] Interactive timeline
- [ ] Zoom/pan capabilities
- [ ] Event details on hover/click

**Current Status:** 🔄 NEED TO VERIFY

---

### Module 4.3: Knowledge Graph
**Required Functionality:**
- [ ] Visual graph showing correlations
- [ ] Nodes: Commit, Config, Error, Service
- [ ] Edges: causal relationships
- [ ] Interactive graph (zoom, pan, select)
- [ ] Using React Flow or similar

**Current Status:** 🔄 NEED TO VERIFY

---

### Module 4.4: Results Screen
**Required Functionality:**
- [ ] Display complete RCA
- [ ] Show risk score with visual indicator
- [ ] Display recommendations
- [ ] Show similar incidents
- [ ] Download PDF button
- [ ] Share/export options

**Current Status:** ✅ IMPLEMENTED (Results.jsx)

---

### Module 4.5: AI Copilot Interface
**Required Functionality:**
- [ ] Chat interface
- [ ] Ask questions about incident
- [ ] Display answers with context
- [ ] Conversation history
- [ ] Suggested questions

**Current Status:** ✅ IMPLEMENTED (Copilot.jsx)

---

## 🔗 Integration Points to Verify

### 1. Member 1 → Member 3
**Required:**
- [ ] Member 1 sends investigation data to Member 3's RCA endpoint
- [ ] Format: GitHub data + Logs + Incident data + Timeline
- [ ] Member 3 receives and processes data
- [ ] Member 3 returns RCA report

**Current Status:** 🔄 NEED TO VERIFY

---

### 2. Member 3 → Member 4
**Required:**
- [ ] Frontend calls Member 3's API endpoints
- [ ] GET /api/health - health check
- [ ] POST /api/generate-rca - generate RCA
- [ ] POST /api/rag/find-similar - find similar incidents
- [ ] POST /api/copilot/ask - ask questions
- [ ] GET /api/pdf/generate-from-incident/{id} - download PDF
- [ ] CORS configured correctly
- [ ] API base URL configured in frontend

**Current Status:** 🔄 NEED TO VERIFY (Check api.js)

---

### 3. Member 2 → Member 1
**Required:**
- [ ] Member 1's Log Agent calls Project 2's logs API
- [ ] GET /logs endpoint accessible
- [ ] Logs returned in expected format
- [ ] Handle authentication if needed

**Current Status:** ⏳ DEPENDS ON MEMBER 2

---

## 📝 Missing Features / Gaps

### Identified Issues:
1. **API Integration in Frontend** - Need to verify frontend is calling correct endpoints
2. **Timeline Visualization** - Need to verify if timeline UI is implemented
3. **Knowledge Graph** - Need to verify if graph visualization exists
4. **Member 1 ↔ Member 3 Integration** - Need to define data contract
5. **Chaos Demo Platform** - Member 2's project is separate (demo application)

---

## ✅ Next Steps

1. **Verify Member 1's Implementation**
   - Check if all 4 agents are complete
   - Verify APIs exist
   - Check data format

2. **Verify Frontend Integration**
   - Check API endpoints in `frontend/src/services/api.js`
   - Verify CORS configuration
   - Test API calls

3. **Update Missing Features**
   - Implement any missing functionality
   - Fix integration issues
   - Add missing UI components

4. **Test End-to-End Flow**
   - Input GitHub URL + Incident
   - Verify entire flow works
   - Fix any broken integration points

---

**Status Legend:**
- ✅ Implemented and verified
- 🔄 Implemented but needs verification
- ⏳ Waiting for dependency
- ❌ Not implemented / Missing

