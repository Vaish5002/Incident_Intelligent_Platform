"""
Full Investigation API - Uses BOTH GitHub Agent AND Log Agent
This is the REAL implementation that actually uses all agents
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
import random
from typing import Optional

# Import the REAL agents
from backend.agents.github_agent import get_github_analysis
from backend.agents.log_agent import get_logs, get_failures
from backend.ai.risk_engine import RiskEngine
from backend.ai.rca_generator import RCAGenerator

router = APIRouter(prefix="/api", tags=["Full Investigation"])


class InvestigationRequest(BaseModel):
    repo_url: str
    incident_description: str


# Storage for investigation results
investigation_store = {}


@router.post("/full-investigate")
async def full_investigate(request: InvestigationRequest):
    """
    Complete investigation using ALL agents:
    1. GitHub Agent - Real commit analysis
    2. Log Agent - Real log processing  
    3. Investigation Engine - Correlation
    4. Risk Scoring - Business impact
    5. Report Generation - RCA document
    """
    try:
        investigation_id = random.randint(1000, 9999)
        logger.info(f"[{investigation_id}] Starting FULL investigation")
        logger.info(f"[{investigation_id}] Repo: {request.repo_url}")
        logger.info(f"[{investigation_id}] Description: {request.incident_description}")
        
        # Store request for async processing
        investigation_store[investigation_id] = {
            "description": request.incident_description,
            "repo_url": request.repo_url,
            "status": "processing"
        }
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "status": "processing",
            "message": "Full investigation started - all agents activated",
            "data": {
                "repo_url": request.repo_url,
                "description": request.incident_description,
                "agents_activated": [
                    "GitHub Agent",
                    "Log Agent", 
                    "Investigation Engine",
                    "Risk Scoring",
                    "Report Generator"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to start investigation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/full-investigations/{investigation_id}")
async def get_full_investigation(investigation_id: int):
    """
    Get results using REAL agents
    """
    try:
        logger.info(f"[{investigation_id}] Fetching results with REAL agents")
        
        # Get stored investigation
        stored = investigation_store.get(investigation_id, {})
        repo_url = stored.get("repo_url", "")
        description = stored.get("description", "")
        
        # =============================================================
        # STEP 1: GITHUB AGENT - Fetch real commits
        # =============================================================
        logger.info(f"[{investigation_id}] Activating GitHub Agent...")
        github_data = get_github_analysis(repo_url, limit=20)
        
        if github_data.get("success"):
            commits_found = github_data.get("total_commits_analyzed", 0)
            config_changes = github_data.get("config_changes", [])
            logger.info(f"[{investigation_id}] ✓ GitHub Agent: Found {commits_found} commits, {len(config_changes)} config changes")
        else:
            logger.warning(f"[{investigation_id}] GitHub Agent failed: {github_data.get('error')}")
            commits_found = 0
            config_changes = []
        
        # =============================================================
        # STEP 2: LOG AGENT - Fetch real logs
        # =============================================================
        logger.info(f"[{investigation_id}] Activating Log Agent...")
        log_data = get_logs(level="ERROR", limit=100, description=description)
        
        error_count = log_data.get("error_count", 0)
        failure_patterns = log_data.get("failure_patterns", {})
        log_timeline = log_data.get("timeline", [])
        logs_source = log_data.get("source", "unknown")
        
        logger.info(f"[{investigation_id}] ✓ Log Agent: Found {error_count} errors (source: {logs_source})")
        logger.info(f"[{investigation_id}] ✓ Failure patterns: {failure_patterns}")
        
        # =============================================================
        # STEP 3: INVESTIGATION ENGINE - Correlate data
        # =============================================================
        logger.info(f"[{investigation_id}] Running Investigation Engine...")
        
        # Correlate GitHub changes with log patterns
        root_cause = _correlate_commits_and_logs(
            github_data, 
            log_data, 
            description
        )
        
        logger.info(f"[{investigation_id}] ✓ Root cause identified: {root_cause}")
        
        # =============================================================
        # STEP 4: RISK SCORING
        # =============================================================
        logger.info(f"[{investigation_id}] Calculating risk score...")
        
        risk_engine = RiskEngine()
        risk_result = risk_engine.calculate_risk(
            incident_description=description,
            logs=f"Found {error_count} errors",
            error_count=error_count,
            affected_service="system"
        )
        
        risk_score = risk_result["risk_score"]
        severity = risk_result["severity"]
        confidence = f"{risk_result['confidence']}%"
        
        logger.info(f"[{investigation_id}] ✓ Risk: {risk_score}/100, Severity: {severity}")
        
        # =============================================================
        # STEP 5: GENERATE RCA REPORT
        # =============================================================
        logger.info(f"[{investigation_id}] Generating RCA report...")
        
        # Build timeline combining GitHub + Logs
        combined_timeline = _build_combined_timeline(github_data, log_data)
        
        # Generate recommendations
        recommendations = _generate_recommendations(
            root_cause,
            github_data,
            log_data
        )
        
        # =============================================================
        # RETURN COMPLETE RESULTS
        # =============================================================
        
        # Get commits for probable_root_cause
        commits = github_data.get("commits", [])
        commit_hash = config_changes[0]["commit"] if config_changes else (commits[0]["sha_short"] if commits else "N/A")
        affected_file = config_changes[0]["file"] if config_changes else "N/A"
        
        # Build GitHub URLs if repo URL is available
        def build_commit_url(sha):
            if repo_url and "github.com" in repo_url:
                return f"{repo_url.rstrip('/')}/commit/{sha}"
            return ""
        
        def build_file_url(sha, filepath):
            if repo_url and "github.com" in repo_url:
                return f"{repo_url.rstrip('/')}/blob/{sha}/{filepath}"
            return ""
        
        # Dynamically compute confidence based on evidence quality
        failure_patterns = log_data.get("failure_patterns", {})
        breakdown = failure_patterns.get("breakdown", {})
        dominant_error = max(breakdown, key=breakdown.get) if breakdown else "UNKNOWN"
        has_config_match = any(cc.get("commit") == commit_hash for cc in config_changes)
        dynamic_confidence = _compute_confidence(
            best_score=min((error_count + commits_found) * 3, 80),
            evidence_count=error_count + commits_found,
            config_match=has_config_match
        )

        probable_root_cause = {
            "description": root_cause,
            "commit": commit_hash,
            "commit_url": build_commit_url(commit_hash) if commit_hash != "N/A" else "",
            "file": affected_file,
            "file_url": build_file_url(commit_hash, affected_file) if commit_hash != "N/A" and affected_file != "N/A" else "",
            "author": config_changes[0].get("author", commits[0]["author"] if commits else "N/A") if config_changes else (commits[0]["author"] if commits else "N/A"),
            "timestamp": config_changes[0].get("timestamp") if config_changes else (commits[0]["date"] if commits else "N/A"),
            "confidence": dynamic_confidence,
            "riskyCodeChanges": _build_risky_code_changes(config_changes, commits),
            "diff": _build_diff_from_commits(config_changes, commits)
        }
        
        result_data = {
            "id": investigation_id,
            "status": "completed",
            "severity": severity,
            "risk_score": risk_score,
            "confidence": confidence,
            "correlation_count": error_count + commits_found,
            "incident_type": _detect_incident_type(description),
            "timeline": combined_timeline,
            "root_cause": root_cause,
            "recommendations": recommendations,
            "probable_root_cause": probable_root_cause,
            "risk_factors": [
                f"Error count: {error_count}",
                f"GitHub config changes: {len(config_changes)}",
                f"Severity: {severity}",
                f"Commits analyzed: {commits_found}"
            ],
            "similar_incidents": [],
            "log_patterns": list(failure_patterns.keys())[:5] if failure_patterns else []
        }
        
        # Save completed result for PDF generation
        investigation_store[investigation_id]["result"] = result_data
        investigation_store[investigation_id]["status"] = "completed"
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "status": "completed",
            "data": {
                "investigation": result_data,
                "root_cause": root_cause,
                "severity": severity
            }
        }
        
    except Exception as e:
        logger.error(f"[{investigation_id}] Investigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Maps log error types to keywords we look for in commit files/messages
_ERROR_KEYWORD_MAP = {
    "TIMEOUT":          ["timeout", "connection", "pool", "db", "database", "query", "sleep", "wait"],
    "CONNECTION_ERROR": ["connection", "socket", "host", "port", "database", "db", "refused", "network"],
    "POOL_EXHAUSTION":  ["pool", "connection", "max_connections", "thread", "executor"],
    "MEMORY_LEAK":      ["memory", "heap", "cache", "buffer", "leak", "allocation"],
    "CPU_SPIKE":        ["cpu", "thread", "loop", "compute", "algorithm", "sort"],
    "GATEWAY_ERROR":    ["gateway", "proxy", "upstream", "nginx", "load", "balancer"],
    "NULL_POINTER":     ["null", "none", "undefined", "pointer", "reference"],
    "UNKNOWN":          [],
}


def _score_commit(commit, desc_lower, dominant_error, config_changes):
    """
    Score a commit 0-100 on how likely it caused the incident.
    Higher = more suspicious.
    """
    score = 0
    sha_short = commit.get("sha_short", "")

    # +30 if this commit has a config change already detected
    for cc in config_changes:
        if cc.get("commit") == sha_short:
            score += 30
            break

    # Keywords from error type
    error_keywords = _ERROR_KEYWORD_MAP.get(dominant_error, [])

    # Score by commit message relevance to description + error keywords
    msg_lower = commit.get("message", "").lower()
    for kw in error_keywords:
        if kw in msg_lower:
            score += 15
    for kw in desc_lower.split():
        if len(kw) > 3 and kw in msg_lower:
            score += 5

    # Score by changed files
    file_score = 0
    for file in commit.get("files_changed", []):
        fname = file.get("filename", "").lower()

        # Skip ALL non-code/non-config file types — these never cause runtime failures
        _NON_CODE_PATTERNS = [
            ".gitignore", ".gitattributes", ".editorconfig",
            "readme", "readme.md", "readme.txt",
            "license", "license.md", "license.txt",
            "changelog", "changelog.md",
            ".md", ".rst", ".txt", ".lock",
            "package-lock.json", "yarn.lock", "poetry.lock",
            "frontend/", "test/", "tests/", "docs/", "__pycache__/",
            ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
            ".pdf", ".docx", ".xlsx",
        ]
        is_non_code = any(p in fname for p in _NON_CODE_PATTERNS)

        # Only allow frontend files if description explicitly mentions frontend/UI
        is_frontend_keyword = any(kw in desc_lower for kw in ["frontend", "theme", "dark", "ui", "css", "color", "style", "button", "page"])
        if is_non_code:
            if "frontend/" in fname and is_frontend_keyword:
                pass  # Allow frontend source files when relevant
            else:
                continue  # Skip everything else

        for kw in error_keywords:
            if kw in fname:
                file_score += 15

        # High-risk file types get a bonus
        if any(pat in fname for pat in ["config", "setting", ".env", "db", "database", "pool", "conn"]):
            file_score += 20

        # Large changes are riskier
        if file.get("changes", 0) > 50:
            file_score += 5

    score += min(file_score, 50)
    return min(score, 100)


def _compute_confidence(best_score, evidence_count, config_match):
    """
    Dynamically compute confidence string based on evidence quality.
    """
    base = best_score  # 0-100
    base += min(evidence_count * 2, 20)  # Up to +20 for volume of evidence
    if config_match:
        base += 15  # Config change is strongest signal
    # Clamp to 40-97%
    pct = max(40, min(97, int(base)))
    return f"{pct}%"


def _correlate_commits_and_logs(github_data, log_data, description):
    """
    Correlate GitHub commits with log failure patterns to identify the most
    likely root cause commit. Scores every commit against:
      - Dominant log error type (CONNECTION_ERROR, TIMEOUT, etc.)
      - Incident description keywords
      - Changed file names
      - Config change detection
    Returns the most suspicious commit's root cause string.
    """
    desc_lower = description.lower()
    config_changes = github_data.get("config_changes", [])
    commits = github_data.get("commits", [])

    # Determine the dominant error type from logs
    failure_patterns = log_data.get("failure_patterns", {})
    breakdown = failure_patterns.get("breakdown", {})
    dominant_error = "UNKNOWN"
    if breakdown:
        dominant_error = max(breakdown, key=breakdown.get)

    error_count = log_data.get("error_count", 0)

    # --- Score every commit ---
    best_commit = None
    best_score = -1

    for commit in commits:
        s = _score_commit(commit, desc_lower, dominant_error, config_changes)
        if s > best_score:
            best_score = s
            best_commit = commit

    # --- Config change match? ---
    config_match = False
    if config_changes and best_commit:
        for cc in config_changes:
            if cc.get("commit") == best_commit.get("sha_short"):
                config_match = True
                change_detail = cc["changes"][0] if cc.get("changes") else "parameter modified"
                if isinstance(change_detail, dict):
                    param = change_detail.get("parameter", "config")
                    old_v = change_detail.get("old_value", "?")
                    new_v = change_detail.get("new_value", "?")
                    detail_str = f"'{param}' changed {old_v} → {new_v}"
                else:
                    detail_str = str(change_detail)
                return (
                    f"Config change in {cc['file']} ({detail_str}) in commit "
                    f"{cc['commit']} correlates with {error_count} "
                    f"{dominant_error} log errors"
                )

    # --- Best scored commit ---
    if best_commit:
        risky_files = [
            f["filename"] for f in best_commit.get("files_changed", [])
            if any(kw in f["filename"].lower() for kw in _ERROR_KEYWORD_MAP.get(dominant_error, []))
        ]
        file_hint = f" — risky files: {', '.join(risky_files[:2])}" if risky_files else ""
        return (
            f"Commit {best_commit['sha_short']} by {best_commit['author']} "
            f"('{best_commit['message'][:80].strip()}'){file_hint} "
            f"correlates with {error_count} {dominant_error} errors in logs"
        )

    # --- Pure description fallback ---
    if "database" in desc_lower or "timeout" in desc_lower:
        return f"Database/connection misconfiguration causing {dominant_error} errors ({error_count} occurrences)"
    elif "memory" in desc_lower:
        return f"Memory leak introducing {dominant_error} errors ({error_count} occurrences)"
    elif "cpu" in desc_lower:
        return f"CPU-intensive operation causing {dominant_error} errors ({error_count} occurrences)"
    else:
        return f"System degradation linked to {dominant_error} errors ({error_count} occurrences)"


def _build_combined_timeline(github_data, log_data):
    """Build timeline from both GitHub and log data"""
    timeline = []
    
    # Add GitHub events
    commits = github_data.get("commits", [])
    if commits:
        timeline.append({
            "time": commits[0]["date"],
            "event": f"Deployment: {commits[0]['message'][:50]}",
            "type": "deployment"
        })
    
    # Add log events (first 5)
    log_timeline = log_data.get("timeline", [])
    timeline.extend(log_timeline[:5])
    
    return timeline


def _generate_recommendations(root_cause, github_data, log_data):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    # Check if there are config changes to rollback
    config_changes = github_data.get("config_changes", [])
    if config_changes:
        commit = config_changes[0]["commit"]
        recommendations.append({
            "priority": "IMMEDIATE",
            "action": f"Rollback commit {commit} to restore previous configuration",
            "impact": "Restore service within 5 minutes"
        })
    
    recommendations.extend([
        {
            "priority": "SHORT-TERM",
            "action": "Review and correct configuration parameters",
            "impact": "Prevent recurrence"
        },
        {
            "priority": "MEDIUM-TERM",
            "action": "Add monitoring alerts for configuration changes",
            "impact": "Early warning system"
        },
        {
            "priority": "LONG-TERM",
            "action": "Implement configuration validation in CI/CD pipeline",
            "impact": "Catch issues before production"
        }
    ])
    
    return recommendations


def _detect_severity(description):
    """Detect severity from description"""
    desc_lower = description.lower()
    if any(word in desc_lower for word in ["critical", "down", "outage", "crash"]):
        return "CRITICAL"
    elif any(word in desc_lower for word in ["error", "failure", "timeout", "leak"]):
        return "HIGH"
    else:
        return "MEDIUM"


def _detect_incident_type(description):
    """Detect incident type from description"""
    desc_lower = description.lower()
    if "database" in desc_lower or "db" in desc_lower:
        return "Database Issue"
    elif "memory" in desc_lower:
        return "Memory Leak"
    elif "cpu" in desc_lower:
        return "CPU Spike"
    elif "network" in desc_lower:
        return "Network Issue"
    else:
        return "System Degradation"


def _build_risky_code_changes(config_changes, commits):
    """Build risky code changes array from GitHub data with actual code snippets"""
    risky_changes = []
    
    # Add config changes as risky changes
    for change in config_changes:
        for param_change in change.get("changes", []):
            if isinstance(param_change, dict):
                risky_changes.append({
                    "file": change["file"],
                    "line": "N/A",
                    "change": f"Parameter '{param_change['parameter']}' changed from '{param_change['old_value']}' to '{param_change['new_value']}'",
                    "severity": "HIGH",
                    "commit": change["commit"],
                    "codeSnippet": {
                        "before": f"{param_change['parameter']}: {param_change['old_value']}",
                        "after": f"{param_change['parameter']}: {param_change['new_value']}",
                        "language": "yaml"
                    },
                    "explanation": f"Changing {param_change['parameter']} from {param_change['old_value']} to {param_change['new_value']} may cause connection exhaustion or timeout issues"
                })
            else:
                risky_changes.append({
                    "file": change["file"],
                    "line": "N/A",
                    "change": str(param_change),
                    "severity": "HIGH",
                    "commit": change["commit"]
                })
    
    # If no config changes, extract actual code from commit patches
    # IMPORTANT: Skip all non-executable file types — they can never cause runtime failures
    _RISKY_EXTENSIONS = (
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".java", ".go", ".rb", ".php", ".c", ".cpp", ".cs",
        ".yaml", ".yml", ".json", ".toml", ".ini", ".conf",
        ".env", ".properties", ".sql", ".sh", ".bash",
    )
    _SKIP_FILENAMES = (
        ".gitignore", ".gitattributes", ".editorconfig",
        "readme", "license", "changelog",
        "package-lock.json", "yarn.lock", "poetry.lock",
    )

    def _is_risky_file(filename):
        fname_lower = filename.lower()
        # Reject non-code files by name
        if any(skip in fname_lower for skip in _SKIP_FILENAMES):
            return False
        # Reject docs / images / media
        if any(fname_lower.endswith(ext) for ext in (".md", ".rst", ".txt", ".lock",
                                                       ".png", ".jpg", ".jpeg", ".gif",
                                                       ".svg", ".ico", ".pdf")):
            return False
        # Accept only known code / config extensions
        return any(fname_lower.endswith(ext) for ext in _RISKY_EXTENSIONS)

    if not risky_changes and commits:
        # Search all recent commits (not just the first) for risky files
        for recent_commit in commits[:5]:
            candidate_files = [
                f for f in recent_commit.get("files_changed", [])
                if _is_risky_file(f["filename"])
            ]
            if candidate_files:
                for file in candidate_files[:3]:  # Top 3 risky files
                    code_snippet = _extract_problematic_code_from_patch(file.get("patch", ""), file["filename"])
                    risky_changes.append({
                        "file": file["filename"],
                        "line": code_snippet.get("line", "N/A"),
                        "change": f"{file['status'].upper()}: {file['additions']} additions, {file['deletions']} deletions",
                        "severity": _calculate_severity_from_file(file),
                        "commit": recent_commit["sha_short"],
                        "codeSnippet": code_snippet,
                        "explanation": _generate_code_explanation(file, code_snippet)
                    })
                break  # Stop at the first commit that has risky files

    return risky_changes


def _build_diff_from_commits(config_changes, commits):
    """Build git diff display from commit data"""
    diff_lines = []
    
    # Show config changes first
    if config_changes:
        change = config_changes[0]
        diff_lines.append(f"diff --git a/{change['file']} b/{change['file']}")
        diff_lines.append(f"--- a/{change['file']}")
        diff_lines.append(f"+++ b/{change['file']}")
        diff_lines.append(f"@@ Commit: {change['commit']} @@")
        
        for param_change in change.get("changes", []):
            if isinstance(param_change, dict):
                diff_lines.append(f"-{param_change['parameter']}: {param_change['old_value']}")
                diff_lines.append(f"+{param_change['parameter']}: {param_change['new_value']}")
    
    # Add commit file changes
    elif commits:
        recent_commit = commits[0]
        files_with_patches = [f for f in recent_commit.get("files_changed", []) if f.get("patch")]
        
        if files_with_patches:
            file = files_with_patches[0]
            diff_lines.append(f"diff --git a/{file['filename']} b/{file['filename']}")
            diff_lines.append(f"--- a/{file['filename']}")
            diff_lines.append(f"+++ b/{file['filename']}")
            diff_lines.append(f"@@ Commit: {recent_commit['sha_short']} by {recent_commit['author']} @@")
            
            # Add full patch with better formatting
            if "patch" in file:
                patch_lines = file["patch"].split('\n')
                diff_lines.extend(patch_lines)
        else:
            # Fallback: show file change summary
            diff_lines.append(f"diff --git a/commit b/{recent_commit['sha_short']}")
            diff_lines.append(f"@@ Commit: {recent_commit['sha_short']} by {recent_commit['author']} @@")
            diff_lines.append(f"Commit Message: {recent_commit['message'][:100]}")
            diff_lines.append(f"Files Changed: {recent_commit['total_files']}")
            diff_lines.append(f"+{recent_commit['total_additions']} additions")
            diff_lines.append(f"-{recent_commit['total_deletions']} deletions")
    else:
        diff_lines = ["No git changes detected in repository."]
    
    return '\n'.join(diff_lines)


def _extract_problematic_code_from_patch(patch, filename):
    """Extract the actual problematic code snippet from git patch"""
    if not patch:
        return {
            "before": "// No patch available",
            "after": "// No patch available",
            "language": _detect_language(filename),
            "line": "N/A"
        }
    
    lines = patch.split('\n')
    before_lines = []
    after_lines = []
    line_number = "N/A"
    
    # Extract line number from @@ header
    for line in lines:
        if line.startswith('@@'):
            import re
            match = re.search(r'@@ -(\d+)', line)
            if match:
                line_number = match.group(1)
            break
    
    # Extract changed lines
    for line in lines:
        if line.startswith('-') and not line.startswith('---'):
            before_lines.append(line[1:].strip())
        elif line.startswith('+') and not line.startswith('+++'):
            after_lines.append(line[1:].strip())
        elif not line.startswith('@@') and not line.startswith('diff') and not line.startswith('index'):
            # Context line
            if before_lines or after_lines:
                before_lines.append(line.strip() if line.strip() else "")
                after_lines.append(line.strip() if line.strip() else "")
    
    # Limit to first 10 lines
    before_code = '\n'.join(before_lines[:10]) if before_lines else "// No changes"
    after_code = '\n'.join(after_lines[:10]) if after_lines else "// No changes"
    
    return {
        "before": before_code,
        "after": after_code,
        "language": _detect_language(filename),
        "line": line_number
    }


def _detect_language(filename):
    """Detect programming language from filename"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.xml': 'xml',
        '.html': 'html',
        '.css': 'css',
        '.sql': 'sql',
        '.sh': 'bash',
    }
    
    for ext, lang in ext_map.items():
        if filename.endswith(ext):
            return lang
    
    return 'text'


def _calculate_severity_from_file(file):
    """Calculate severity based on file changes"""
    changes = file.get("changes", 0)
    filename = file.get("filename", "").lower()
    
    # High risk indicators
    if any(keyword in filename for keyword in ['config', 'database', 'auth', 'security']):
        return "HIGH"
    
    # Medium risk for large changes
    if changes > 50:
        return "MEDIUM"
    
    return "LOW"


def _generate_code_explanation(file, code_snippet):
    """Generate explanation of what the code change might cause"""
    filename = file.get("filename", "").lower()
    status = file.get("status", "modified")
    
    # Config file explanations
    if 'config' in filename or 'yml' in filename or 'yaml' in filename:
        return "Configuration changes can affect system behavior, connection pools, timeouts, or resource limits"
    
    # Database file explanations
    if 'database' in filename or 'db' in filename or 'sql' in filename:
        return "Database-related changes may impact query performance, connection handling, or data integrity"
    
    # Code file explanations
    if status == "modified":
        additions = file.get("additions", 0)
        deletions = file.get("deletions", 0)
        if additions > deletions:
            return f"Added {additions - deletions} lines of code which may introduce new logic or dependencies"
        elif deletions > additions:
            return f"Removed {deletions - additions} lines of code which may affect existing functionality"
        else:
            return "Modified code logic which may change application behavior"
    elif status == "added":
        return "New file added which introduces new functionality or dependencies"
    elif status == "deleted":
        return "File deleted which may break dependencies or remove required functionality"
    
    return "Code change may affect application behavior or performance"


class ChaosInjectionRequest(BaseModel):
    type: str
    duration_seconds: Optional[int] = 300


@router.post("/chaos/inject-failure")
async def inject_failure_proxy(request: ChaosInjectionRequest):
    """
    Proxy chaos failure injection to the configured PROJECT2_URL (Chaos Demo Platform)
    """
    import requests
    from backend.agents.log_agent import PROJECT2_URL
    
    # Map 'db_timeout' -> 'db-timeout', 'memory_leak' -> 'memory-leak', etc.
    failure_type_hyphenated = request.type.replace("_", "-")
    
    # Clean the URL
    target_url = f"{PROJECT2_URL.rstrip('/')}/inject/{failure_type_hyphenated}"
    logger.info(f"Proxying failure injection to: {target_url}")
    
    try:
        response = requests.post(target_url, json={"duration_seconds": request.duration_seconds}, timeout=10)
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "status": "injected",
                "message": f"Successfully injected {request.type} into Chaos Platform",
                "details": response.json()
            }
        else:
            logger.error(f"Chaos Platform returned status {response.status_code}: {response.text}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Chaos Platform returned error: {response.text}"
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to Chaos Platform at {target_url}: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Chaos Platform at {PROJECT2_URL} is unreachable: {str(e)}"
        )
