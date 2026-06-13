import requests
import os
from datetime import datetime, timedelta

# Project 2 URL - can be configured via environment variable
PROJECT2_URL = os.environ.get("PROJECT2_URL", "https://project2.onrender.com")


def get_logs(service=None, level="ERROR", limit=100):
    """
    Fetch logs from Project 2 (Chaos Demo Platform).
    Falls back to mock data if Project 2 is unavailable.
    
    Args:
        service: Filter by service name (optional)
        level: Log level (ERROR, WARNING, INFO) - default ERROR
        limit: Maximum number of logs to return
    
    Returns:
        Dictionary with logs, failure patterns, and summary
    """
    try:
        # Try to fetch from Project 2
        params = {"level": level, "limit": limit}
        if service:
            params["service"] = service
        
        response = requests.get(
            f"{PROJECT2_URL}/logs",
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            logs_data = response.json()
            parsed_logs = _parse_logs(logs_data)
            
            return {
                "success": True,
                "source": "project2_api",
                "total_logs": len(parsed_logs),
                "error_count": sum(1 for log in parsed_logs if log["level"] == "ERROR"),
                "warning_count": sum(1 for log in parsed_logs if log["level"] == "WARNING"),
                "logs": parsed_logs,
                "failure_patterns": _detect_failure_patterns(parsed_logs),
                "timeline": _build_log_timeline(parsed_logs)
            }
        else:
            # Project 2 returned error, use fallback
            return _get_fallback_logs(service, level, limit)
    
    except requests.exceptions.RequestException as e:
        # Project 2 unavailable, use fallback
        print(f"Project 2 unavailable: {str(e)}, using mock data")
        return _get_fallback_logs(service, level, limit)


def get_failures():
    """Fetch failure events from Project 2"""
    try:
        response = requests.get(f"{PROJECT2_URL}/failures", timeout=5)
        if response.status_code == 200:
            return {
                "success": True,
                "failures": response.json()
            }
    except:
        pass
    
    return {
        "success": False,
        "failures": _get_mock_failures()
    }


def get_status():
    """Check Project 2 status"""
    try:
        response = requests.get(f"{PROJECT2_URL}/status", timeout=5)
        if response.status_code == 200:
            return {
                "success": True,
                "status": response.json()
            }
    except:
        pass
    
    return {
        "success": False,
        "status": "unavailable"
    }


def _parse_logs(logs_data):
    """Parse and structure log entries"""
    parsed_logs = []
    
    # Handle different response formats
    if isinstance(logs_data, list):
        logs = logs_data
    elif isinstance(logs_data, dict) and "logs" in logs_data:
        logs = logs_data["logs"]
    else:
        logs = []
    
    for log in logs:
        if isinstance(log, dict):
            parsed_logs.append({
                "timestamp": log.get("timestamp", datetime.now().isoformat()),
                "level": log.get("level", "ERROR"),
                "message": log.get("message", ""),
                "service": log.get("service", "unknown"),
                "error_type": _categorize_error(log.get("message", ""))
            })
        elif isinstance(log, str):
            parsed_logs.append({
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR",
                "message": log,
                "service": "unknown",
                "error_type": _categorize_error(log)
            })
    
    return parsed_logs


def _categorize_error(message):
    """Categorize error based on message content"""
    if not message:
        return "UNKNOWN"
    
    message_lower = message.lower()
    
    if "timeout" in message_lower:
        return "TIMEOUT"
    elif "memory" in message_lower or "oom" in message_lower:
        return "MEMORY_LEAK"
    elif "connection" in message_lower or "refused" in message_lower:
        return "CONNECTION_ERROR"
    elif "pool" in message_lower and "exhaust" in message_lower:
        return "POOL_EXHAUSTION"
    elif "null" in message_lower or "pointer" in message_lower:
        return "NULL_POINTER"
    elif "gateway" in message_lower:
        return "GATEWAY_ERROR"
    elif "cpu" in message_lower or "spike" in message_lower:
        return "CPU_SPIKE"
    else:
        return "UNKNOWN"


def _detect_failure_patterns(logs):
    """Detect patterns in failure logs"""
    patterns = {}
    
    for log in logs:
        error_type = log.get("error_type", "UNKNOWN")
        patterns[error_type] = patterns.get(error_type, 0) + 1
    
    # Sort by frequency
    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "most_common": sorted_patterns[0] if sorted_patterns else ("UNKNOWN", 0),
        "breakdown": dict(sorted_patterns),
        "total_types": len(patterns)
    }


def _build_log_timeline(logs):
    """Build timeline from logs"""
    if not logs:
        return []
    
    # Sort by timestamp
    sorted_logs = sorted(logs, key=lambda x: x.get("timestamp", ""))
    
    timeline = []
    for log in sorted_logs[:20]:  # Limit to first 20 for timeline
        timeline.append({
            "time": log.get("timestamp"),
            "event": f"{log.get('level')}: {log.get('message')[:50]}...",
            "type": "error"
        })
    
    return timeline


def _get_fallback_logs(service=None, level="ERROR", limit=100):
    """Generate realistic mock logs when Project 2 is unavailable"""
    base_time = datetime.now() - timedelta(minutes=30)
    
    mock_logs = [
        {
            "timestamp": (base_time + timedelta(minutes=i)).isoformat(),
            "level": "ERROR",
            "message": msg,
            "service": svc,
            "error_type": _categorize_error(msg)
        }
        for i, (msg, svc) in enumerate([
            ("Database connection timeout after 30s", "payment-service"),
            ("Connection pool exhausted: max_connections=10 reached", "payment-service"),
            ("Failed to acquire database connection", "payment-service"),
            ("Database Timeout: Query exceeded 30s limit", "payment-service"),
            ("Connection refused: Database not responding", "payment-service"),
            ("Payment processing failed: Database unavailable", "payment-service"),
            ("Transaction rollback: Connection lost", "payment-service"),
            ("Database Timeout on SELECT query", "payment-service"),
        ])
    ]
    
    # Filter by service if specified
    if service:
        mock_logs = [log for log in mock_logs if log["service"] == service]
    
    # Limit results
    mock_logs = mock_logs[:limit]
    
    return {
        "success": True,
        "source": "fallback_mock",
        "total_logs": len(mock_logs),
        "error_count": len(mock_logs),
        "warning_count": 0,
        "logs": mock_logs,
        "failure_patterns": _detect_failure_patterns(mock_logs),
        "timeline": _build_log_timeline(mock_logs),
        "note": "Using mock data - Project 2 unavailable"
    }


def _get_mock_failures():
    """Mock failure events"""
    return [
        {
            "type": "DB_TIMEOUT",
            "timestamp": datetime.now().isoformat(),
            "count": 8
        }
    ]