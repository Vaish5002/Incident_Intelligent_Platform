def classify_incident(description):
    """
    Classify incident to determine type, severity, and impact.
    
    Args:
        description: Incident description from user
    
    Returns:
        Dictionary with incident type, affected service, severity, and impact
    """
    description_lower = description.lower()
    
    # Default classification
    classification = {
        "incident_type": "Unknown",
        "affected_service": "unknown",
        "severity": "Low",
        "business_impact": "Minor Issue",
        "confidence": 0.5
    }
    
    # Payment failures
    if any(word in description_lower for word in ["payment", "checkout", "transaction", "billing"]):
        classification = {
            "incident_type": "Payment Failure",
            "affected_service": "payment-service",
            "severity": "Critical",
            "business_impact": "Revenue Loss",
            "user_impact": "Users unable to complete purchases",
            "confidence": 0.95
        }
    
    # Database issues
    elif any(word in description_lower for word in ["database", "db", "timeout", "connection pool", "query"]):
        classification = {
            "incident_type": "Database Issue",
            "affected_service": "database",
            "severity": "High",
            "business_impact": "Service Disruption",
            "user_impact": "Slow response times or failures",
            "confidence": 0.90
        }
    
    # Memory leaks
    elif any(word in description_lower for word in ["memory leak", "oom", "out of memory", "memory"]):
        classification = {
            "incident_type": "Memory Leak",
            "affected_service": "application-server",
            "severity": "High",
            "business_impact": "Performance Degradation",
            "user_impact": "Slow application performance",
            "confidence": 0.85
        }
    
    # API/Gateway issues
    elif any(word in description_lower for word in ["gateway", "api", "502", "503", "504"]):
        classification = {
            "incident_type": "Gateway Failure",
            "affected_service": "api-gateway",
            "severity": "Critical",
            "business_impact": "Service Unavailable",
            "user_impact": "Cannot access application",
            "confidence": 0.90
        }
    
    # Authentication issues
    elif any(word in description_lower for word in ["auth", "login", "authentication", "token"]):
        classification = {
            "incident_type": "Authentication Failure",
            "affected_service": "auth-service",
            "severity": "High",
            "business_impact": "Access Denied",
            "user_impact": "Users cannot login",
            "confidence": 0.85
        }
    
    # Null pointer / crashes
    elif any(word in description_lower for word in ["null pointer", "crash", "exception", "error"]):
        classification = {
            "incident_type": "Application Crash",
            "affected_service": "application",
            "severity": "High",
            "business_impact": "Service Disruption",
            "user_impact": "Application crashes or errors",
            "confidence": 0.80
        }
    
    # CPU spikes
    elif any(word in description_lower for word in ["cpu", "spike", "high load", "performance"]):
        classification = {
            "incident_type": "CPU Spike",
            "affected_service": "compute",
            "severity": "Medium",
            "business_impact": "Performance Degradation",
            "user_impact": "Slow response times",
            "confidence": 0.75
        }
    
    # Network issues
    elif any(word in description_lower for word in ["network", "connection", "unreachable"]):
        classification = {
            "incident_type": "Network Issue",
            "affected_service": "network",
            "severity": "High",
            "business_impact": "Service Disruption",
            "user_impact": "Cannot reach services",
            "confidence": 0.80
        }
    
    # Configuration issues
    elif any(word in description_lower for word in ["config", "configuration", "env", "missing"]):
        classification = {
            "incident_type": "Configuration Error",
            "affected_service": "configuration",
            "severity": "Medium",
            "business_impact": "Service Misconfiguration",
            "user_impact": "Partial functionality loss",
            "confidence": 0.75
        }
    
    return classification