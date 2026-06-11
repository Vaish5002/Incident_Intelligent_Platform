"""
Auto remove duplicate folders without confirmation
"""
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent

duplicates = ['backend', 'frontend', 'agents']
removed = []

print("Removing duplicate folders...")

for folder_name in duplicates:
    folder_path = ROOT_DIR / folder_name
    
    if folder_path.exists() and folder_path.is_dir():
        try:
            print(f"  Removing {folder_name}/...", end=" ")
            shutil.rmtree(folder_path)
            removed.append(folder_name)
            print("Done")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"  {folder_name}/ not found (already removed)")

print(f"\nRemoved {len(removed)} duplicate folders: {', '.join(removed)}")
