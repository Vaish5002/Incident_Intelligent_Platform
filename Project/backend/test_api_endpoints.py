"""
Quick API endpoint test
"""
import requests
import json

BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_risk_score():
    """Test risk score endpoint"""
    print("\n=== Testing Risk Score Endpoint ===")
    data = {
        "incident": "Database connection timeout",
        "logs": "Connection pool exhausted, timeout after 30s",
        "affected_service": "payment",
        "error_count": 243
    }
    
    response = requests.post(f"{BASE_URL}/api/risk-score", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nRisk Assessment:")
        print(f"  Severity: {result['severity']}")
        print(f"  Risk Score: {result['risk_score']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Factors: {', '.join(result['factors'])}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_quick_rca():
    """Test quick RCA endpoint"""
    print("\n=== Testing Quick RCA Endpoint ===")
    data = {
        "incident": "Payment service timeout",
        "logs": "502 Bad Gateway errors",
        "timeline": "Load spike -> Timeout -> Errors"
    }
    
    response = requests.post(f"{BASE_URL}/api/quick-rca", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nQuick RCA Preview (first 300 chars):")
        print(result['rca_text'][:300])
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("API Endpoint Tests".center(70))
    print("=" * 70)
    
    results = []
    
    # Test 1: Health
    results.append(("Health", test_health()))
    
    # Test 2: Risk Score
    results.append(("Risk Score", test_risk_score()))
    
    # Test 3: Quick RCA
    results.append(("Quick RCA", test_quick_rca()))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary".center(70))
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n SUCCESS: All API endpoints working!")
    else:
        print("\n FAILURE: Some endpoints failed")
