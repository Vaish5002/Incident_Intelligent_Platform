# SmartOps AI - Backend

FastAPI-based backend service with AI-powered incident investigation.

## Structure

```
backend/
├── agents/              # Investigation agents
│   ├── classification_agent.py
│   ├── github_agent.py
│   ├── log_agent.py
│   ├── investigation_agent.py
│   ├── investigation_engine.py
│   └── timeline_agent.py
├── ai/                  # AI services
│   ├── config.py
│   ├── gemini_service.py
│   ├── rag_service.py
│   ├── rca_generator.py
│   ├── risk_engine.py
│   ├── pdf_generator.py
│   ├── embedding_service.py
│   ├── knowledge_base.py
│   └── member1_integration.py
├── api/                 # API routes
│   ├── demo_investigate_routes.py
│   ├── rca_routes.py
│   ├── pdf_routes.py
│   └── ...
├── database/            # Database models
│   ├── connection.py
│   └── models.py
├── schemas/             # Pydantic schemas
│   ├── rca.py
│   ├── risk.py
│   └── knowledge.py
├── main.py              # FastAPI application
├── run_server.py        # Development server
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── render.yaml          # Render deployment config
├── Procfile             # Process configuration
└── runtime.txt          # Python version

```

## Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run Server

```bash
python run_server.py
```

Server runs at: http://localhost:8002  
API Docs: http://localhost:8002/docs

## Environment Variables

Required:
- `GEMINI_API_KEY` - Google Gemini API key

Optional:
- `GEMINI_MODEL` - Model name (default: gemini-flash-latest)
- `API_HOST` - Host address (default: 0.0.0.0)
- `API_PORT` - Port number (default: 8002)
- `DEBUG` - Debug mode (default: True)
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins

## API Endpoints

- `POST /api/investigate` - Start new investigation
- `GET /api/investigations/{id}` - Get investigation results
- `GET /api/pdf/generate-from-incident/{id}` - Download PDF report
- `POST /api/generate-rca` - Generate RCA report
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

## Features

- 7 Failure Type Analysis (Database, Memory, CPU, API, Cache, Network, Disk)
- Contextual RCA Generation
- PDF Report Generation
- Historical Incident Search (RAG)
- Risk Scoring
- AI-Powered Recommendations

## Deployment

See [deployment documentation](../../STEP_BY_STEP_DEPLOYMENT.md) for detailed instructions.

### Render Deployment

```bash
# Automatic via render.yaml
# Just connect GitHub repository
```

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Start with uvicorn
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Testing

```bash
# Run all tests
pytest

# Run specific test
python test_api_endpoints.py
```

## Tech Stack

- FastAPI - Web framework
- Google Gemini Pro - LLM
- SQLite - Database
- SQLAlchemy - ORM
- Sentence Transformers - Embeddings
- ReportLab - PDF generation
- Pydantic - Data validation

## License

MIT
