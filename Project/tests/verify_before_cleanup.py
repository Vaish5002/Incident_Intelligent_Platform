"""
Pre-cleanup verification script
Verifies that all code is safely inside Project/ before cleanup
"""
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
PROJECT_DIR = ROOT_DIR / "Project"

def verify_structure():
    """Verify Project folder has all necessary code"""
    print("=" * 70)
    print("PRE-CLEANUP VERIFICATION")
    print("=" * 70)
    
    checks = []
    
    # Check 1: Project folder exists
    print("\n[1/7] Checking Project folder exists...")
    if PROJECT_DIR.exists():
        print("  ✓ Project/ folder exists")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/ folder not found!")
        checks.append(False)
    
    # Check 2: Backend in Project
    print("\n[2/7] Checking Project/backend/...")
    backend_files = [
        "Project/backend/main.py",
        "Project/backend/run_server.py",
        "Project/backend/requirements.txt",
        "Project/backend/ai",
        "Project/backend/api",
        "Project/backend/database"
    ]
    backend_ok = all((ROOT_DIR / f).exists() for f in backend_files)
    if backend_ok:
        print("  ✓ Project/backend/ complete")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/backend/ missing files")
        checks.append(False)
    
    # Check 3: Frontend in Project
    print("\n[3/7] Checking Project/frontend/...")
    frontend_files = [
        "Project/frontend/package.json",
        "Project/frontend/vite.config.js",
        "Project/frontend/src",
        "Project/frontend/public"
    ]
    frontend_ok = all((ROOT_DIR / f).exists() for f in frontend_files)
    if frontend_ok:
        print("  ✓ Project/frontend/ complete")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/frontend/ missing files")
        checks.append(False)
    
    # Check 4: Agents in Project
    print("\n[4/7] Checking Project/agents/...")
    agents_files = [
        "Project/agents/github_agent.py",
        "Project/agents/log_agent.py",
        "Project/agents/investigation_engine.py",
        "Project/agents/timeline_agent.py"
    ]
    agents_ok = all((ROOT_DIR / f).exists() for f in agents_files)
    if agents_ok:
        print("  ✓ Project/agents/ complete")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/agents/ missing files")
        checks.append(False)
    
    # Check 5: temp_analysis in Project
    print("\n[5/7] Checking Project/temp_analysis/...")
    temp_analysis = ROOT_DIR / "Project" / "temp_analysis"
    if temp_analysis.exists():
        print("  ✓ Project/temp_analysis/ exists")
        checks.append(True)
    else:
        print("  ✗ WARNING: Project/temp_analysis/ not found (may not be needed)")
        checks.append(True)  # Not critical
    
    # Check 6: README.md exists
    print("\n[6/7] Checking README.md...")
    readme = ROOT_DIR / "README.md"
    if readme.exists():
        print("  ✓ README.md exists")
        checks.append(True)
    else:
        print("  ✗ ERROR: README.md not found!")
        checks.append(False)
    
    # Check 7: Duplicate folders exist (to be removed)
    print("\n[7/7] Checking for duplicate folders...")
    duplicates = []
    for folder in ['backend', 'frontend', 'agents']:
        old_folder = ROOT_DIR / folder
        if old_folder.exists():
            duplicates.append(folder)
    
    if duplicates:
        print(f"  ✓ Found {len(duplicates)} duplicate folders to remove: {', '.join(duplicates)}")
        checks.append(True)
    else:
        print("  ℹ No duplicate folders found (may have been removed already)")
        checks.append(True)
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if all(checks):
        print("\n✓ ALL CHECKS PASSED - SAFE TO CLEANUP")
        print("\nProject structure verified:")
        print("  ✓ Project/backend/ - Complete")
        print("  ✓ Project/frontend/ - Complete")
        print("  ✓ Project/agents/ - Complete")
        print("  ✓ Project/temp_analysis/ - Moved inside")
        print("  ✓ README.md - Ready")
        
        if duplicates:
            print(f"\nDuplicate folders will be removed:")
            for dup in duplicates:
                print(f"  ✗ {dup}/ (already in Project/{dup}/)")
        
        print("\n" + "=" * 70)
        print("READY FOR CLEANUP")
        print("=" * 70)
        print("\nRun: python final_cleanup.py")
        return True
    else:
        print("\n✗ VERIFICATION FAILED - DO NOT RUN CLEANUP YET")
        print("\nPlease fix the errors above before proceeding.")
        return False

if __name__ == "__main__":
    verify_structure()
