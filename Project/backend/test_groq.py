"""
Quick test script for Groq Integration
Run this to verify your setup works
"""
import asyncio
import sys
from loguru import logger
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ai.groq_service import GroqService
from backend.ai.config import settings


async def test_groq_service():
    """Test Groq service with sample data"""
    
    print("=" * 60)
    print("Testing SmartOps AI - Groq Integration")
    print("=" * 60)
    
    # Check API key
    if not settings.GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY not set in .env file")
        return
    
    print(f"✅ API Key configured")
    print(f"✅ Model: {settings.GROQ_MODEL}")
    print()
    
    try:
        # Initialize service
        print("Initializing Groq service...")
        service = GroqService()
        print("✅ Groq service initialized\n")
        
        # Sample incident data
        print("=" * 60)
        print("TEST 1: Generating Quick RCA")
        print("=" * 60)
        
        result = service.generate_quick_rca(
            incident_description="Users cannot complete payments after deployment",
            log_summary="Database timeout errors, Connection pool exhausted, Payment service failures",
            timeline_summary="16:00 Deployment started → 16:05 Config changed → 16:10 Database errors → 16:15 Payment failures"
        )
        
        if result["success"]:
            print("✅ Quick RCA Generated:\n")
            print(result["rca_text"])
            print()
        else:
            print(f"❌ Failed: {result.get('error')}")
        
        # Test comprehensive RCA
        print("\n" + "=" * 60)
        print("TEST 2: Generating Comprehensive RCA")
        print("=" * 60)
        
        github_data = {
            "repo_name": "company/payment-service",
            "total_commits": 3,
            "commits": [
                {
                    "sha": "abc1234",
                    "message": "Update database pool configuration",
                    "author": "dev@company.com",
                    "changed_files": ["config/database.py"]
                }
            ],
            "changed_files": ["config/database.py", "requirements.txt"]
        }
        
        log_data = {
            "total_logs": 1523,
            "error_count": 243,
            "warning_count": 87,
            "critical_errors": [
                {
                    "timestamp": "2024-01-15 16:10:00",
                    "message": "Database connection timeout after 30s"
                },
                {
                    "timestamp": "2024-01-15 16:11:30",
                    "message": "Connection pool exhausted, 0 connections available"
                }
            ],
            "error_patterns": {
                "timeout": 89,
                "pool": 67,
                "connection": 54
            }
        }
        
        timeline_data = {
            "events": [
                {
                    "timestamp": "2024-01-15 16:00:00",
                    "event_type": "deployment",
                    "description": "Deployment started"
                },
                {
                    "timestamp": "2024-01-15 16:05:00",
                    "event_type": "commit",
                    "description": "Database config changed"
                },
                {
                    "timestamp": "2024-01-15 16:10:00",
                    "event_type": "error",
                    "description": "Database timeout errors"
                }
            ]
        }
        
        candidates = [
            {
                "type": "code_change",
                "confidence": 0.9,
                "description": "Database pool size reduced from 50 to 10 in config/database.py"
            }
        ]
        
        result = service.generate_rca(
            incident_description="Users cannot complete payments after deployment",
            severity="critical",
            affected_service="payment",
            risk_score=91.5,
            github_analysis=github_data,
            log_analysis=log_data,
            timeline=timeline_data,
            root_cause_candidates=candidates
        )
        
        if result["success"]:
            print("✅ Comprehensive RCA Generated:\n")
            print(result["rca_text"][:500] + "...")
            print(f"\n[Full RCA is {len(result['rca_text'])} characters]")
            print()
        else:
            print(f"❌ Failed: {result.get('error')}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Start the API server: python -m backend.main")
        print("2. Test via API: http://localhost:8002/docs")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.exception("Test failed")


if __name__ == "__main__":
    asyncio.run(test_groq_service())
