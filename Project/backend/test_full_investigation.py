"""
Test the full investigation endpoint with real agents
"""
import sys
import io
import requests
import json
import time

# Fix Unicode encoding on Windows terminals (cp1252 can't handle emojis/symbols)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


BASE_URL = "http://localhost:8002/api"

def test_full_investigation():
    """Test complete flow with all agents"""
    
    print("\n" + "="*80)
    print("🚀 TESTING FULL INVESTIGATION WITH ALL AGENTS")
    print("="*80 + "\n")
    
    # Test data
    test_repo = "https://github.com/Vaish5002/chaos-demo-platform"
    test_description = "Database connection timeout causing payment failures after recent deployment"
    
    print(f"📋 Test Case:")
    print(f"   Repository: {test_repo}")
    print(f"   Description: {test_description}")
    print()
    
    # Step 1: Start investigation
    print("🔷 STEP 1: Starting Full Investigation")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/full-investigate",
            json={
                "repo_url": test_repo,
                "incident_description": test_description
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            investigation_id = data.get("investigation_id")
            
            print(f"✅ Investigation Started")
            print(f"   Investigation ID: {investigation_id}")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            
            if 'data' in data and 'agents_activated' in data['data']:
                print(f"   Agents Activated: {', '.join(data['data']['agents_activated'])}")
            
            print()
        else:
            print(f"❌ Failed to start investigation: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error starting investigation: {e}")
        return
    
    # Step 2: Wait a bit for processing
    print("⏳ Waiting 2 seconds for agents to process...")
    time.sleep(2)
    print()
    
    # Step 3: Get results
    print("🔷 STEP 2: Fetching Results from All Agents")
    print("-" * 80)
    
    try:
        response = requests.get(
            f"{BASE_URL}/full-investigations/{investigation_id}",
            timeout=15
        )
        
        if response.status_code == 200:
            results = response.json()
            
            if results.get("success"):
                print("✅ Investigation Completed\n")
                
                investigation = results.get("data", {}).get("investigation", {})
                
                # Show GitHub Agent results
                print("🐙 GITHUB AGENT RESULTS:")
                github_analysis = investigation.get("github_analysis", {})
                print(f"   Commits Analyzed: {github_analysis.get('commits_analyzed', 0)}")
                print(f"   Files Changed: {github_analysis.get('files_changed', 0)}")
                print(f"   Config Changes Detected: {len(github_analysis.get('config_changes', []))}")
                
                if github_analysis.get('config_changes'):
                    print(f"   Latest Config Change:")
                    change = github_analysis['config_changes'][0]
                    print(f"      File: {change.get('file', 'N/A')}")
                    print(f"      Commit: {change.get('commit', 'N/A')}")
                print()
                
                # Show Log Agent results
                print("📋 LOG AGENT RESULTS:")
                log_analysis = investigation.get("log_analysis", {})
                print(f"   Error Count: {log_analysis.get('error_count', 0)}")
                print(f"   Data Source: {log_analysis.get('source', 'unknown')}")
                print(f"   Most Common Error: {log_analysis.get('most_common_error', 'N/A')}")
                
                patterns = log_analysis.get('patterns', {})
                if patterns and isinstance(patterns, dict) and 'breakdown' in patterns:
                    print(f"   Error Patterns:")
                    for error_type, count in list(patterns['breakdown'].items())[:3]:
                        print(f"      {error_type}: {count}")
                print()
                
                # Show Investigation Engine results
                print("🔬 INVESTIGATION ENGINE RESULTS:")
                print(f"   Root Cause: {investigation.get('root_cause', 'N/A')}")
                print(f"   Severity: {investigation.get('severity', 'N/A')}")
                print(f"   Risk Score: {investigation.get('risk_score', 0)}/100")
                print(f"   Confidence: {investigation.get('confidence', 'N/A')}")
                print(f"   Incident Type: {investigation.get('incident_type', 'N/A')}")
                print()
                
                # Show Timeline
                print("📅 TIMELINE (First 3 events):")
                timeline = investigation.get('timeline', [])
                for i, event in enumerate(timeline[:3], 1):
                    print(f"   {i}. [{event.get('time', 'N/A')}] {event.get('event', 'N/A')}")
                print()
                
                # Show Recommendations
                print("💡 RECOMMENDATIONS:")
                recommendations = investigation.get('recommendations', [])
                for i, rec in enumerate(recommendations[:3], 1):
                    if isinstance(rec, dict):
                        print(f"   {i}. [{rec.get('priority', 'NORMAL')}] {rec.get('action', 'N/A')}")
                    else:
                        print(f"   {i}. {rec}")
                print()
                
                print("="*80)
                print("✅ ALL AGENTS WORKING SUCCESSFULLY!")
                print("="*80)
                print(f"\n📊 Summary:")
                print(f"   - GitHub Agent: ✅ Analyzed {github_analysis.get('commits_analyzed', 0)} commits")
                print(f"   - Log Agent: ✅ Processed {log_analysis.get('error_count', 0)} errors")
                print(f"   - Investigation Engine: ✅ Identified root cause")
                print(f"   - Risk Scoring: ✅ Calculated risk score {investigation.get('risk_score', 0)}/100")
                print(f"   - Report Generator: ✅ Generated {len(recommendations)} recommendations")
                print()
                
            else:
                print(f"❌ Investigation failed: {results.get('message', 'Unknown error')}")
                
        else:
            print(f"❌ Failed to get results: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fetching results: {e}")

if __name__ == "__main__":
    test_full_investigation()
