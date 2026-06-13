from github import Github
import re
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Get GitHub token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get_github_analysis(repo_url, limit=20):
    """
    Fetch detailed GitHub commit analysis with file changes and config detection.
    
    Args:
        repo_url: GitHub repository URL
        limit: Number of recent commits to fetch (default 20)
    
    Returns:
        Dictionary with commits, config changes, and summary
    """
    try:
        # Parse repository URL
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo_name = parts[-1]

        # Use token if available (5000 requests/hour), otherwise anonymous (60 requests/hour)
        if GITHUB_TOKEN:
            g = Github(GITHUB_TOKEN)
        else:
            g = Github()
        
        repo = g.get_repo(f"{owner}/{repo_name}")

        commits_data = []
        config_changes = []

        # Fetch recent commits (up to limit)
        for commit in repo.get_commits()[:limit]:
            files_changed = []
            
            # Extract file changes
            for file in commit.files:
                file_info = {
                    "filename": file.filename,
                    "status": file.status,  # added, modified, removed, renamed
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes
                }
                
                # Add patch if available (first 500 chars)
                if file.patch:
                    file_info["patch"] = file.patch[:500]
                
                files_changed.append(file_info)
                
                # Detect config changes
                if _is_config_file(file.filename) and file.patch:
                    detected_changes = _extract_config_changes(file.patch, file.filename)
                    if detected_changes:
                        config_changes.append({
                            "commit": commit.sha[:7],
                            "file": file.filename,
                            "author": commit.commit.author.name,
                            "changes": detected_changes,
                            "timestamp": str(commit.commit.author.date)
                        })
            
            # Build commit data
            commit_data = {
                "sha": commit.sha,
                "sha_short": commit.sha[:7],
                "message": commit.commit.message,
                "author": commit.commit.author.name,
                "email": commit.commit.author.email,
                "date": str(commit.commit.author.date),
                "files_changed": files_changed,
                "total_files": len(files_changed),
                "total_additions": sum(f["additions"] for f in files_changed),
                "total_deletions": sum(f["deletions"] for f in files_changed)
            }
            
            commits_data.append(commit_data)

        return {
            "success": True,
            "repository": repo_url,
            "total_commits_analyzed": len(commits_data),
            "commits": commits_data,
            "config_changes": config_changes,
            "summary": {
                "total_files_changed": sum(c["total_files"] for c in commits_data),
                "total_additions": sum(c["total_additions"] for c in commits_data),
                "total_deletions": sum(c["total_deletions"] for c in commits_data),
                "config_changes_detected": len(config_changes)
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "repository": repo_url
        }


def _is_config_file(filename):
    """Check if file is a configuration file"""
    config_patterns = [
        r'config',
        r'\.env',
        r'\.yaml',
        r'\.yml',
        r'\.json',
        r'\.ini',
        r'\.conf',
        r'\.properties',
        r'settings',
        r'\.toml'
    ]
    filename_lower = filename.lower()
    return any(re.search(pattern, filename_lower) for pattern in config_patterns)


def _extract_config_changes(patch, filename):
    """Extract configuration parameter changes from patch"""
    changes = []
    
    # Common config patterns
    patterns = [
        (r'[-](\w+)\s*[=:]\s*(\S+)', r'[+](\w+)\s*[=:]\s*(\S+)'),  # KEY = VALUE
        (r'[-](\w+):\s*(\S+)', r'[+](\w+):\s*(\S+)'),  # KEY: VALUE (YAML)
        (r'[-]\s*"?(\w+)"?\s*:\s*"?([^"]+)"?', r'[+]\s*"?(\w+)"?\s*:\s*"?([^"]+)"?'),  # JSON
    ]
    
    lines = patch.split('\n')
    
    for i, line in enumerate(lines):
        # Look for removed lines (-)
        if line.startswith('-') and not line.startswith('---'):
            # Look for corresponding added line (+)
            for j in range(i, min(i + 5, len(lines))):
                if lines[j].startswith('+') and not lines[j].startswith('+++'):
                    # Try to extract key-value changes
                    old_match = re.search(r'(\w+)\s*[=:]\s*(\S+)', line)
                    new_match = re.search(r'(\w+)\s*[=:]\s*(\S+)', lines[j])
                    
                    if old_match and new_match and old_match.group(1) == new_match.group(1):
                        changes.append({
                            "parameter": old_match.group(1),
                            "old_value": old_match.group(2),
                            "new_value": new_match.group(2)
                        })
                    break
    
    return changes