"""
Remove ONLY duplicate folders (backend, frontend, agents) from root
Keeps everything else untouched
"""
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent

def remove_duplicate_folders():
    """Remove only backend/, frontend/, agents/ from root (duplicates of Project/)"""
    print("=" * 70)
    print("REMOVE DUPLICATE FOLDERS")
    print("=" * 70)
    print("\nThis will ONLY remove duplicate code folders:")
    print("  ✗ backend/ (duplicate of Project/backend/)")
    print("  ✗ frontend/ (duplicate of Project/frontend/)")
    print("  ✗ agents/ (duplicate of Project/agents/)")
    print("\nEverything else will remain untouched:")
    print("  ✓ Resume/ folder")
    print("  ✓ docs/ folder")
    print("  ✓ All .md, .txt, .bat files")
    print("  ✓ temp_analysis/ (already moved to Project/)")
    print("  ✓ All other files and folders")
    
    confirm = input("\nAre you sure? Type 'YES' to continue: ")
    if confirm != 'YES':
        print("Operation cancelled.")
        return
    
    duplicates = ['backend', 'frontend', 'agents']
    removed = []
    not_found = []
    errors = []
    
    print("\n" + "=" * 70)
    print("REMOVING DUPLICATE FOLDERS")
    print("=" * 70)
    
    for folder_name in duplicates:
        folder_path = ROOT_DIR / folder_name
        
        if not folder_path.exists():
            not_found.append(folder_name)
            print(f"  ℹ {folder_name}/ - Not found (may already be removed)")
            continue
        
        if not folder_path.is_dir():
            print(f"  ⚠ {folder_name} - Is a file, not a folder. Skipping.")
            continue
        
        try:
            print(f"  🗑 Removing {folder_name}/ ...", end=" ")
            shutil.rmtree(folder_path)
            removed.append(folder_name)
            print("✓ Done")
        except Exception as e:
            errors.append(f"{folder_name}: {e}")
            print(f"✗ Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)
    
    if removed:
        print(f"\n✓ Removed {len(removed)} duplicate folder(s):")
        for folder in removed:
            print(f"  ✗ {folder}/")
    
    if not_found:
        print(f"\nℹ {len(not_found)} folder(s) not found (already removed?):")
        for folder in not_found:
            print(f"  - {folder}/")
    
    if errors:
        print(f"\n✗ {len(errors)} error(s) occurred:")
        for error in errors:
            print(f"  ! {error}")
    
    print("\n" + "=" * 70)
    print("CURRENT STRUCTURE")
    print("=" * 70)
    print("""
Incident_Intelligent_Platform/
├── Project/                (ALL YOUR CODE - ONLY COPY)
│   ├── backend/           ✓ Original code here
│   ├── frontend/          ✓ Original code here
│   ├── agents/            ✓ Original code here
│   └── temp_analysis/     ✓ Moved here
├── Resume/                 ✓ Kept untouched
├── docs/                   ✓ Kept untouched
├── All .md files           ✓ Kept untouched
├── All .txt files          ✓ Kept untouched
└── All other files         ✓ Kept untouched
    """)
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Verify Project/ folder has all code:
   - cd Project/backend && dir
   - cd Project/frontend && dir
   - cd Project/agents && dir

2. Test applications work from Project/ folder:
   - cd Project/backend && python run_server.py
   - cd Project/frontend && npm run dev

3. Push to GitHub:
   - git status
   - git add .
   - git commit -m "Removed duplicate folders - all code in Project/"
   - git push origin main
    """)

if __name__ == "__main__":
    remove_duplicate_folders()
