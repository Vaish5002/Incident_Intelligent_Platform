from agents.classification_agent import classify_incident
from datetime import datetime


def generate_investigation(incident_description, github_data, log_data):
    """
    Comprehensive investigation engine that correlates GitHub, logs, and incident data.
    
    Args:
        incident_description: User's incident description
        github_data: Data from GitHub agent
        log_data: Data from log agent
    
    Returns:
        Complete investigation report with timeline and correlation
    """
    # 1. Classify the incident
    classification = classify_incident(incident_description)
    
    # 2. Build timeline from GitHub + Logs
    timeline = _build_timeline(github_data, log_data)
    
    # 3. Correlate commits with errors
    correlation = _correlate_events(github_data, log_data)
    
    # 4. Identify probable root cause
    root_cause = _identify_root_cause(correlation, classification, github_data, log_data)
    
    # 5. Summarize data
    github_summary = _summarize_github(github_data)
    log_summary = _summarize_logs(log_data)
    
    # 6. Calculate overall confidence
    confidence = _calculate_confidence(correlation, classification)
    
    return {
        "incident_type": classification["incident_type"],
        "affected_service": classification["affected_service"],
        "severity": classification["severity"],
        "business_impact": classification["business_impact"],
        "user_impact": classification.get("user_impact", "Unknown"),
        "confidence": confidence,
        "timeline": timeline,
        "correlation": correlation,
        "probable_root_cause": root_cause,
        "github_summary": github_summary,
        "log_summary": log_summary,
        "classification_confidence": classification.get("confidence", 0.5)
    }


def _build_timeline(github_data, log_data):
    """Build chronological timeline of all events"""
    events = []
    
    # Add deployment events from GitHub
    if github_data.get("success") and github_data.get("commits"):
        for commit in github_data["commits"][:10]:  # Limit to 10 most recent
            events.append({
                "timestamp": commit["date"],
                "type": "deployment",
                "description": f"Code deployed: {commit['message'][:50]}...",
                "details": {
                    "commit_sha": commit["sha_short"],
                    "author": commit["author"],
                    "files_changed": commit["total_files"]
                }
            })
    
    # Add config change events
    if github_data.get("config_changes"):
        for config in github_data["config_changes"]:
            events.append({
                "timestamp": config["timestamp"],
                "type": "config_change",
                "description": f"Config modified: {config['file']}",
                "details": {
                    "commit": config["commit"],
                    "file": config["file"],
                    "changes": config["changes"]
                }
            })
    
    # Add error events from logs
    if log_data.get("logs"):
        for log in log_data["logs"][:20]:  # Limit to 20 most recent errors
            events.append({
                "timestamp": log["timestamp"],
                "type": "error",
                "description": log["message"][:60],
                "details": {
                    "level": log["level"],
                    "service": log["service"],
                    "error_type": log["error_type"]
                }
            })
    
    # Sort by timestamp
    try:
        events.sort(key=lambda x: x["timestamp"])
    except:
        pass  # If timestamp parsing fails, keep original order
    
    return events


def _correlate_events(github_data, log_data):
    """Find correlations between commits and errors"""
    correlations = []
    
    if not github_data.get("success") or not github_data.get("commits"):
        return correlations
    
    if not log_data.get("logs"):
        return correlations
    
    commits = github_data["commits"]
    logs = log_data["logs"]
    
    # Simple correlation: check if error messages relate to changed files
    for log in logs[:10]:  # Check first 10 errors
        log_message = log.get("message", "").lower()
        error_type = log.get("error_type", "")
        
        for commit in commits[:5]:  # Check recent 5 commits
            # Check if commit changed relevant files
            relevant_files = []
            for file_change in commit.get("files_changed", []):
                filename = file_change.get("filename", "").lower()
                
                # Database-related
                if error_type == "TIMEOUT" and any(word in filename for word in ["db", "database", "config"]):
                    relevant_files.append(file_change["filename"])
                
                # Memory-related
                elif error_type == "MEMORY_LEAK" and any(word in filename for word in ["memory", "cache", "pool"]):
                    relevant_files.append(file_change["filename"])
                
                # General matching
                elif any(word in log_message for word in ["config", "database", "connection"] if word in filename):
                    relevant_files.append(file_change["filename"])
            
            if relevant_files:
                correlations.append({
                    "commit_sha": commit["sha_short"],
                    "commit_message": commit["message"][:60],
                    "error_message": log["message"][:60],
                    "error_type": error_type,
                    "relevant_files": relevant_files,
                    "confidence": 0.8 if len(relevant_files) > 1 else 0.6
                })
    
    # Sort by confidence
    correlations.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    
    return correlations[:5]  # Return top 5 correlations


def _identify_root_cause(correlation, classification, github_data, log_data):
    """Identify the most probable root cause"""
    
    # If we have strong correlation
    if correlation and correlation[0].get("confidence", 0) > 0.7:
        top = correlation[0]
        return {
            "description": f"Likely caused by commit {top['commit_sha']}: {top['commit_message']}. "
                          f"This commit modified {', '.join(top['relevant_files'][:2])} "
                          f"which correlates with {top['error_type']} errors.",
            "commit": top["commit_sha"],
            "files": top["relevant_files"],
            "confidence": top["confidence"],
            "evidence": "Strong correlation between code changes and error pattern"
        }
    
    # If we have config changes
    elif github_data.get("config_changes"):
        config = github_data["config_changes"][0]
        changes_desc = ", ".join([f"{c['parameter']}: {c['old_value']} → {c['new_value']}" 
                                  for c in config["changes"][:2]])
        return {
            "description": f"Configuration change detected in {config['file']}: {changes_desc}. "
                          f"This may have caused {classification['incident_type']}.",
            "commit": config["commit"],
            "files": [config["file"]],
            "confidence": 0.75,
            "evidence": "Configuration change detected before incident"
        }
    
    # Based on error patterns
    elif log_data.get("failure_patterns"):
        pattern = log_data["failure_patterns"].get("most_common", ("UNKNOWN", 0))
        return {
            "description": f"Multiple {pattern[0]} errors detected ({pattern[1]} occurrences). "
                          f"This suggests {classification['incident_type']} issue.",
            "confidence": 0.6,
            "evidence": f"Error pattern: {pattern[0]} repeated {pattern[1]} times"
        }
    
    # Fallback
    else:
        return {
            "description": f"Based on incident description, this appears to be a {classification['incident_type']} "
                          f"affecting {classification['affected_service']}.",
            "confidence": classification.get("confidence", 0.5),
            "evidence": "Based on incident classification"
        }


def _summarize_github(github_data):
    """Summarize GitHub analysis"""
    if not github_data.get("success"):
        return {"error": github_data.get("error", "GitHub analysis failed")}
    
    return {
        "total_commits": github_data.get("total_commits_analyzed", 0),
        "total_files_changed": github_data.get("summary", {}).get("total_files_changed", 0),
        "config_changes_detected": len(github_data.get("config_changes", [])),
        "recent_commit": github_data["commits"][0]["message"][:60] if github_data.get("commits") else "None"
    }


def _summarize_logs(log_data):
    """Summarize log analysis"""
    return {
        "total_logs": log_data.get("total_logs", 0),
        "error_count": log_data.get("error_count", 0),
        "warning_count": log_data.get("warning_count", 0),
        "most_common_error": log_data.get("failure_patterns", {}).get("most_common", ["Unknown", 0])[0],
        "source": log_data.get("source", "unknown")
    }


def _calculate_confidence(correlation, classification):
    """Calculate overall investigation confidence"""
    scores = []
    
    # Correlation confidence
    if correlation:
        scores.append(correlation[0].get("confidence", 0))
    
    # Classification confidence
    scores.append(classification.get("confidence", 0.5))
    
    # Average confidence
    if scores:
        return round(sum(scores) / len(scores), 2)
    else:
        return 0.5