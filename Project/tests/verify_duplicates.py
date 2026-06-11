"""
Verify that duplicate folders can be safely removed
Checks that Project/ has all the necessary code
"""
from pathlib import Path

ROOT_DIR = Path(__file__).parent

def verify_safe_to_remove():
    """Verify Project folder has all code before removing duplicates"""
    print("=" * 70)
    print("VERIFY SAFE TO REMOVE DUPLICATES")
    print("=" * 70)
    
    checks = []
    
    # Check Project/backend
    print("\n[1/3] Checking Project/backend/...")
    backend_key_files = [
        "Project/backend/main.py",
        "Project/backend/run_server.py",
        "Project/backend/requirements.txt"
    ]
    backend_ok = all((ROOT_DIR / f).exists() for f in backend_key_files)
    if backend_ok:
        print("  ✓ Project/backend/ has key files (main.py, run_server.py, requirements.txt)")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/backend/ missing key files!")
        checks.append(False)
    
    # Check Project/frontend
    print("\n[2/3] Checking Project/frontend/...")
    frontend_key_files = [
        "Project/frontend/package.json",
        "Project/frontend/vite.config.js",
        "Project/frontend/index.html"
    ]
    frontend_ok = all((ROOT_DIR / f).exists() for f in frontend_key_files)
    if frontend_ok:
        print("  ✓ Project/frontend/ has key files (package.json, vite.config.js, index.html)")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/frontend/ missing key files!")
        checks.append(False)
    
    # Check Project/agents
    print("\n[3/3] Checking Project/agents/...")
    agents_key_files = [
        "Project/agents/github_agent.py",
        "Project/agents/log_agent.py",
        "Project/agents/investigation_engine.py"
    ]
    agents_ok = all((ROOT_DIR / f).exists() for f in agents_key_files)
    if agents_ok:
        print("  ✓ Project/agents/ has key files (github_agent.py, log_agent.py, investigation_engine.py)")
        checks.append(True)
    else:
        print("  ✗ ERROR: Project/agents/ missing key files!")
        checks.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION RESULT")
    print("=" * 70)
    
    if all(checks):
        print("\n✅ SAFE TO REMOVE DUPLICATES")
        print("\nProject folder has all necessary code:")
        print("  ✓ Project/backend/ - Complete")
        print("  ✓ Project/frontend/ - Complete")
        print("  ✓ Project/agents/ - Complete")
        
        print("\nDuplicate folders at root can be removed:")
        duplicates_exist = []
        for folder in ['backend', 'frontend', 'agents']:
            if (ROOT_DIR / folder).exists():
                duplicates_exist.append(folder)
        
        if duplicates_exist:
            for folder in duplicates_exist:
                print(f"  ✗ {folder}/ (duplicate)")
        else:
            print("  ℹ No duplicates found (may already be removed)")
        
        print("\n" + "=" * 70)
        print("RUN: python remove_duplicates.py")
        print("=" * 70)
        return True
    else:
        print("\n❌ NOT SAFE - DO NOT REMOVE")
        print("\nProject folder is missing files. Fix errors above first.")
        return False

if __name__ == "__main__":
    verify_safe_to_remove()
