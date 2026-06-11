"""
Project cleanup script - Removes temporary documentation and test files
Run this before committing to GitHub
"""
import os
import shutil
from pathlib import Path

# Root directory
ROOT_DIR = Path(__file__).parent

# Patterns for files to remove
REMOVE_PATTERNS = [
    # Temporary markdown files
    '*_STATUS.md', '*_COMPLETE.md', '*_SUMMARY.md', '*_VERIFICATION.md',
    '*_ANALYSIS.md', '*_REPORT.md', '*_READY.md', '*_SUCCESS.md',
    '*_FIXED.md', 'DEMO_*.md', 'START_*.md', 'QUICK_*.md', 'LIVE_*.md',
    'APPLY_*.md', 'FIX_*.md', 'GAP*.md', 'INTEGRATION_*.md',
    'MEMBER*_*.md', 'MODULE*_*.md', 'PROJECT*_*.md', 'CURRENT_*.md',
    'FINAL_*.md', 'ENHANCED_*.md', 'VISUAL_*.md', 'COMPLETE_*.md',
    'EVERYTHING_*.md', 'BRANCH_*.md', 'CORS_*.md', 'CONTEXT_*.md',
    'NETWORK_*.md', 'NEXT_*.md', 'FRONTEND_*.md', 'API_*.md',
    'ARCHITECTURE_*.md', 'PRESENTATION_*.md', 'CLEANUP_*.md',
    'WHERE_*.md', 'MASTER_*.md', 'EXECUTIVE_*.md', 'FLOW_*.md',
    'GIT_*.md', 'GITHUB_*.md', 'TEST_RESULTS_*.md', 'REQUIREMENTS_*.md',
    'SETUP_*.md', 'APPLICATION_*.md',
    
    # Temporary text files (keep requirements.txt)
    '*.txt',
    
    # Test scripts in root (keep in backend)
    'test_*.py',
    
    # Batch files
    'restart_*.bat', 'start_all_*.bat',
    
    # Database files
    '*.db', '*.sqlite', '*.sqlite3',
    
    # PDF files
    '*.pdf',
]

# Keep these files
KEEP_FILES = {
    'README.md',
    'requirements.txt',
    '.gitignore',
    '.env.example',
    'LICENSE',
    'CONTRIBUTING.md',
    'CHANGELOG.md',
}

# Keep these directories
KEEP_DIRS = {
    '.git',
    'backend',
    'frontend',
    'agents',
    'docs',
    '.vscode',
    'node_modules',
    '__pycache__',
    'venv',
    'env',
}

# Directories to remove completely
REMOVE_DIRS = {
    'Resume',
    'temp_analysis',
    'temp',
    'tmp',
    '__pycache__',
}

def should_remove_file(file_path: Path) -> bool:
    """Check if file should be removed"""
    
    # Always keep certain files
    if file_path.name in KEEP_FILES:
        return False
    
    # Check patterns
    for pattern in REMOVE_PATTERNS:
        if file_path.match(pattern):
            # Special case: keep requirements.txt
            if file_path.name == 'requirements.txt':
                return False
            # Special case: keep test files in backend
            if 'test_' in file_path.name and 'backend' in str(file_path):
                return False
            return True
    
    return False

def cleanup():
    """Clean up temporary files"""
    print("=" * 60)
    print("PROJECT CLEANUP SCRIPT")
    print("=" * 60)
    
    removed_files = []
    removed_dirs = []
    errors = []
    
    # Remove specified directories
    print("\nRemoving temporary directories...")
    for dir_name in REMOVE_DIRS:
        dir_path = ROOT_DIR / dir_name
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
                removed_dirs.append(str(dir_path))
                print(f"  Removed directory: {dir_name}")
            except Exception as e:
                errors.append(f"Failed to remove {dir_name}: {e}")
    
    # Remove files matching patterns
    print("\nRemoving temporary files...")
    for file_path in ROOT_DIR.glob('*'):
        if file_path.is_file() and should_remove_file(file_path):
            try:
                file_path.unlink()
                removed_files.append(str(file_path.name))
                print(f"  Removed file: {file_path.name}")
            except Exception as e:
                errors.append(f"Failed to remove {file_path.name}: {e}")
    
    # Remove __pycache__ directories recursively
    print("\nRemoving __pycache__ directories...")
    for pycache in ROOT_DIR.rglob('__pycache__'):
        if pycache.is_dir():
            try:
                shutil.rmtree(pycache)
                removed_dirs.append(str(pycache))
                print(f"  Removed: {pycache}")
            except Exception as e:
                errors.append(f"Failed to remove {pycache}: {e}")
    
    # Remove .pyc files
    print("\nRemoving .pyc files...")
    for pyc_file in ROOT_DIR.rglob('*.pyc'):
        try:
            pyc_file.unlink()
            removed_files.append(str(pyc_file))
        except Exception as e:
            errors.append(f"Failed to remove {pyc_file}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("CLEANUP SUMMARY")
    print("=" * 60)
    print(f"Files removed: {len(removed_files)}")
    print(f"Directories removed: {len(removed_dirs)}")
    
    if errors:
        print(f"\nErrors: {len(errors)}")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
    
    print("\n" + "=" * 60)
    print("CLEANUP COMPLETE!")
    print("=" * 60)
    print("\nProject structure cleaned. Ready for GitHub push.")
    print("\nNext steps:")
    print("1. Review changes: git status")
    print("2. Stage changes: git add .")
    print("3. Commit: git commit -m 'Project cleanup and documentation'")
    print("4. Push: git push origin main")

if __name__ == "__main__":
    confirm = input("This will remove temporary files. Continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        cleanup()
    else:
        print("Cleanup cancelled.")
