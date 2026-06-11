"""
Final cleanup script - Removes everything except Project folder and README.md
This prepares the repository for GitHub push with clean structure
"""
import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent

# Keep only these items
KEEP_ITEMS = {
    'Project',
    'README.md',
    '.git',
    '.gitignore',
    'final_cleanup.py',
    '.env'  # Keep root .env if it exists
}

def final_cleanup():
    """Remove all files except Project folder and README.md"""
    print("=" * 70)
    print("FINAL PROJECT CLEANUP")
    print("=" * 70)
    print("\nThis will remove ALL files and folders except:")
    print("  - Project/ folder (all your code + temp_analysis)")
    print("  - README.md")
    print("  - .git/ folder")
    print("  - .gitignore")
    print("\nEverything else will be deleted, including:")
    print("  - backend/ folder (duplicate - already in Project/)")
    print("  - frontend/ folder (duplicate - already in Project/)")
    print("  - agents/ folder (duplicate - already in Project/)")
    print("  - Resume/ folder")
    print("  - docs/ folder")
    print("  - All .md, .txt, .bat files")
    
    confirm = input("\nAre you sure? Type 'YES' to continue: ")
    if confirm != 'YES':
        print("Cleanup cancelled.")
        return
    
    removed_files = []
    removed_dirs = []
    errors = []
    
    print("\nStarting cleanup...")
    
    # Iterate through all items in root directory
    for item in ROOT_DIR.iterdir():
        item_name = item.name
        
        # Skip items we want to keep
        if item_name in KEEP_ITEMS:
            print(f"  ✓ Keeping: {item_name}")
            continue
        
        # Remove files
        if item.is_file():
            try:
                item.unlink()
                removed_files.append(item_name)
                print(f"  ✗ Removed file: {item_name}")
            except Exception as e:
                errors.append(f"Failed to remove {item_name}: {e}")
        
        # Remove directories (including duplicate backend, frontend, agents)
        elif item.is_dir():
            try:
                # Special message for duplicate folders
                if item_name in ['backend', 'frontend', 'agents']:
                    print(f"  ✗ Removing DUPLICATE: {item_name}/ (code already in Project/{item_name}/)")
                else:
                    print(f"  ✗ Removed directory: {item_name}/")
                shutil.rmtree(item)
                removed_dirs.append(item_name)
            except Exception as e:
                errors.append(f"Failed to remove {item_name}: {e}")
    
    # Clean up __pycache__ in Project folder
    print("\nCleaning __pycache__ from Project folder...")
    project_dir = ROOT_DIR / "Project"
    if project_dir.exists():
        for pycache in project_dir.rglob('__pycache__'):
            try:
                shutil.rmtree(pycache)
                print(f"  Removed: {pycache}")
            except Exception as e:
                errors.append(f"Failed to remove {pycache}: {e}")
    
    # Remove .db files from Project
    print("\nRemoving database files from Project folder...")
    for db_file in project_dir.rglob('*.db'):
        try:
            db_file.unlink()
            print(f"  Removed: {db_file}")
        except Exception as e:
            errors.append(f"Failed to remove {db_file}: {e}")
    
    # Remove .pyc files from Project
    print("\nRemoving .pyc files from Project folder...")
    for pyc_file in project_dir.rglob('*.pyc'):
        try:
            pyc_file.unlink()
        except Exception as e:
            errors.append(f"Failed to remove {pyc_file}: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)
    print(f"\nFiles removed: {len(removed_files)}")
    print(f"Directories removed: {len(removed_dirs)}")
    
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for error in errors[:10]:
            print(f"  - {error}")
    
    print("\n" + "=" * 70)
    print("FINAL STRUCTURE:")
    print("=" * 70)
    print("""
Incident_Intelligent_Platform/
├── .git/                    (Git repository)
├── .gitignore              (Git exclusions)
├── .env                    (Environment variables)
├── Project/                (ALL YOUR CODE)
│   ├── backend/           (FastAPI backend - ONLY COPY)
│   ├── frontend/          (React frontend - ONLY COPY)
│   ├── agents/            (Investigation agents - ONLY COPY)
│   └── temp_analysis/     (Analysis files)
└── README.md               (Project documentation)

Note: Duplicate folders (backend/, frontend/, agents/) removed from root.
    """)
    
    print("=" * 70)
    print("READY FOR GITHUB")
    print("=" * 70)
    print("\nNext steps:")
    print("1. git status")
    print("2. git add .")
    print("3. git commit -m 'Clean project structure'")
    print("4. git push origin main")
    print("\nOnly README.md and Project/ folder will be in GitHub!")

if __name__ == "__main__":
    final_cleanup()
