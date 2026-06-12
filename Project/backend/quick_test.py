"""
Quick API test for Groq
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ai.groq_service import GroqService

print("=" * 60)
print("Quick Groq API Test")
print("=" * 60)

try:
    service = GroqService()
    print("Service initialized successfully")
    
    print("\n--- Test 1: Quick RCA ---")
    result = service.generate_quick_rca(
        incident_description="Payment failures after deployment",
        log_summary="Database timeout, connection pool exhausted",
        timeline_summary="16:00 Deploy -> 16:05 Config change -> 16:10 Errors"
    )
    
    if result["success"]:
        print("SUCCESS - Quick RCA generated!")
        print("\nResponse preview:")
        print(result["rca_text"][:500])
    else:
        print(f"FAILED: {result.get('error')}")
    
    print("\n\n--- Test 2: Recommendations ---")
    result2 = service.generate_recommendations(
        root_cause="Database pool size reduced from 50 to 10",
        severity="critical",
        affected_service="payment"
    )
    
    if result2["success"]:
        print("SUCCESS - Recommendations generated!")
        print("\nResponse preview:")
        print(result2["recommendations"][:500])
    else:
        print(f"FAILED: {result2.get('error')}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)

except Exception as e:
    print(f"ERROR: {e}")
