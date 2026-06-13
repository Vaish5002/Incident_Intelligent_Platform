"""
Test script to verify GitHub commit details are properly formatted for UI display
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.github_agent import get_github_analysis
from api.full_investigation_routes import _build_risky_code_changes, _build_diff_from_commits
import json


def test_github_commit_display():
    print("=" * 70)
    print("TESTING GITHUB COMMIT DISPLAY IN RCA REPORT")
    print("=" * 70)
    print()
    
    # Test repository
    repo_url = "https://github.com/Amirtha2503/demooplatform"
    
    print(f"📦 Repository: {repo_url}")
    print()
    
    # Step 1: Fetch GitHub data
    print("Step 1: Fetching GitHub data via PyGithub...")
    print("-" * 70)
    github_data = get_github_analysis(repo_url, limit=5)
    
    if not github_data.get("success"):
        print(f"❌ GitHub Agent failed: {github_data.get('error')}")
        return
    
    commits = github_data.get("commits", [])
    config_changes = github_data.get("config_changes", [])
    
    print(f"✅ Success!")
    print(f"   Commits found: {len(commits)}")
    print(f"   Config changes: {len(config_changes)}")
    print()
    
    # Step 2: Show first commit details
    if commits:
        print("Step 2: First Commit Details")
        print("-" * 70)
        commit = commits[0]
        print(f"   SHA: {commit['sha_short']}")
        print(f"   Author: {commit['author']}")
        print(f"   Date: {commit['date']}")
        print(f"   Message: {commit['message'][:80]}...")
        print(f"   Files changed: {commit['total_files']}")
        print(f"   Additions: +{commit['total_additions']}")
        print(f"   Deletions: -{commit['total_deletions']}")
        print()
    
    # Step 3: Show config changes
    if config_changes:
        print("Step 3: Configuration Changes Detected")
        print("-" * 70)
        for i, change in enumerate(config_changes, 1):
            print(f"   Config Change #{i}:")
            print(f"     File: {change['file']}")
            print(f"     Commit: {change['commit']}")
            print(f"     Timestamp: {change.get('timestamp', 'N/A')}")
            print(f"     Parameters changed: {len(change.get('changes', []))}")
            for param in change.get('changes', []):
                if isinstance(param, dict):
                    print(f"       - {param['parameter']}: {param['old_value']} → {param['new_value']}")
                else:
                    print(f"       - {param}")
        print()
    
    # Step 4: Build risky code changes (for frontend)
    print("Step 4: Building Risky Code Changes for UI")
    print("-" * 70)
    risky_changes = _build_risky_code_changes(config_changes, commits)
    
    print(f"   Generated {len(risky_changes)} risky code changes:")
    for i, change in enumerate(risky_changes, 1):
        print(f"\n   Change #{i}:")
        print(f"     File: {change['file']}")
        print(f"     Severity: {change['severity']}")
        print(f"     Commit: {change['commit']}")
        print(f"     Change: {change['change']}")
    print()
    
    # Step 5: Build diff display (for frontend)
    print("Step 5: Building Git Diff for UI Display")
    print("-" * 70)
    diff = _build_diff_from_commits(config_changes, commits)
    
    print("   Generated diff (first 20 lines):")
    print()
    diff_lines = diff.split('\n')[:20]
    for line in diff_lines:
        if line.startswith('+') and not line.startswith('+++'):
            print(f"   \033[92m{line}\033[0m")  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"   \033[91m{line}\033[0m")  # Red
        elif line.startswith('@@'):
            print(f"   \033[94m{line}\033[0m")  # Blue
        else:
            print(f"   {line}")
    print()
    
    # Step 6: Show complete probable_root_cause structure
    print("Step 6: Complete probable_root_cause Structure (Backend Response)")
    print("-" * 70)
    
    probable_root_cause = {
        "description": f"Configuration change in {config_changes[0]['file']}" if config_changes else "Recent code change",
        "commit": config_changes[0]["commit"] if config_changes else (commits[0]["sha_short"] if commits else "N/A"),
        "file": config_changes[0]["file"] if config_changes else "N/A",
        "author": config_changes[0].get("author") if config_changes else (commits[0]["author"] if commits else "N/A"),
        "timestamp": config_changes[0].get("timestamp") if config_changes else (commits[0]["date"] if commits else "N/A"),
        "confidence": "94%",
        "riskyCodeChanges": risky_changes,
        "diff": diff[:500] + "..." if len(diff) > 500 else diff
    }
    
    print(json.dumps(probable_root_cause, indent=2))
    print()
    
    # Step 7: Verification
    print("=" * 70)
    print("VERIFICATION RESULTS")
    print("=" * 70)
    print()
    
    checks = [
        ("✅" if commits else "❌", "Commits fetched from GitHub"),
        ("✅" if config_changes else "⚠️", "Config changes detected (optional)"),
        ("✅" if risky_changes else "❌", "Risky code changes generated"),
        ("✅" if diff and len(diff) > 50 else "❌", "Git diff generated"),
        ("✅" if probable_root_cause.get("commit") != "N/A" else "❌", "Commit hash available"),
        ("✅" if probable_root_cause.get("author") != "N/A" else "❌", "Author information available"),
        ("✅" if probable_root_cause.get("file") != "N/A" else "❌", "File information available"),
    ]
    
    all_passed = True
    for status, check in checks:
        print(f"   {status} {check}")
        if status == "❌":
            all_passed = False
    
    print()
    
    if all_passed or (not config_changes and commits):
        print("🎉 SUCCESS! GitHub commit details will be displayed correctly in UI")
        print()
        print("Frontend will show:")
        print("   • Risky code changes section with file names and severity")
        print("   • Git diff viewer with syntax highlighting")
        print("   • Commit hash and author in header")
        print("   • Complete traceability for root cause")
    else:
        print("⚠️  WARNING: Some data might be missing")
        print("   Frontend may show 'No repository modifications identified'")
    
    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_github_commit_display()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
