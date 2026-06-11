"""
Risk Scoring Engine
Calculates severity, risk score, and confidence for incidents
"""
from typing import Dict, Any, Optional, List
from loguru import logger
import re


class RiskEngine:
    """
    Risk scoring engine that analyzes incidents and assigns:
    - Severity level (Low/Medium/High/Critical)
    - Risk score (0-100)
    - Confidence level (0-100)
    """
    
    # Severity levels
    SEVERITY_CRITICAL = "Critical"
    SEVERITY_HIGH = "High"
    SEVERITY_MEDIUM = "Medium"
    SEVERITY_LOW = "Low"
    
    # Keywords for severity classification
    CRITICAL_KEYWORDS = [
        "database timeout", "database failure", "db timeout", "connection timeout",
        "payment failure", "payment failed", "transaction failed",
        "service down", "service unavailable", "outage", "crash",
        "data loss", "data corruption", "security breach",
        "authentication failure", "authorization failed", "auth failed",
        "cannot connect", "connection refused", "connection failed"
    ]
    
    HIGH_KEYWORDS = [
        "memory leak", "high memory", "out of memory", "oom",
        "high cpu", "cpu spike", "performance degradation",
        "slow response", "timeout", "latency",
        "error rate", "high error", "multiple errors",
        "disk full", "storage full"
    ]
    
    MEDIUM_KEYWORDS = [
        "warning", "deprecated", "retry", "fallback",
        "degraded", "partial failure", "intermittent",
        "queue full", "backlog", "delay"
    ]
    
    LOW_KEYWORDS = [
        "info", "debug", "trace", "notice",
        "startup", "shutdown", "configuration"
    ]
    
    def __init__(self):
        """Initialize risk engine"""
        logger.info("Risk engine initialized")
    
    def calculate_risk(
        self,
        incident_description: str,
        logs: Optional[str] = None,
        affected_service: Optional[str] = None,
        error_count: Optional[int] = None,
        user_impact: Optional[str] = None,
        business_impact: Optional[str] = None,
        timeline_events: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score for an incident
        
        Args:
            incident_description: Description of the incident
            logs: Log summary or error messages
            affected_service: Service affected (payment, auth, etc.)
            error_count: Number of errors detected
            user_impact: Description of user impact
            business_impact: Description of business impact
            timeline_events: List of timeline events
            
        Returns:
            Dictionary with severity, risk_score, confidence, and breakdown
        """
        logger.info("Calculating risk score for incident")
        
        # Combine all text for analysis
        combined_text = self._combine_text(
            incident_description, logs, affected_service, 
            user_impact, business_impact
        )
        
        # Calculate individual risk factors
        severity_score = self._calculate_severity_score(combined_text)
        service_score = self._calculate_service_score(affected_service)
        error_score = self._calculate_error_score(error_count)
        impact_score = self._calculate_impact_score(user_impact, business_impact)
        timeline_score = self._calculate_timeline_score(timeline_events)
        
        # Calculate weighted risk score
        risk_score = self._calculate_weighted_score(
            severity_score=severity_score,
            service_score=service_score,
            error_score=error_score,
            impact_score=impact_score,
            timeline_score=timeline_score
        )
        
        # Determine severity level
        severity = self._determine_severity(risk_score, combined_text)
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            incident_description, logs, error_count, 
            affected_service, timeline_events
        )
        
        result = {
            "severity": severity,
            "risk_score": round(risk_score, 2),
            "confidence": round(confidence, 2),
            "breakdown": {
                "severity_score": round(severity_score, 2),
                "service_score": round(service_score, 2),
                "error_score": round(error_score, 2),
                "impact_score": round(impact_score, 2),
                "timeline_score": round(timeline_score, 2)
            },
            "factors": self._identify_risk_factors(combined_text)
        }
        
        logger.info(f"Risk calculated: {severity} (score: {risk_score}, confidence: {confidence})")
        return result
    
    def _combine_text(
        self,
        incident: str,
        logs: Optional[str],
        service: Optional[str],
        user_impact: Optional[str],
        business_impact: Optional[str]
    ) -> str:
        """Combine all text inputs for analysis"""
        parts = [incident or ""]
        if logs:
            parts.append(logs)
        if service:
            parts.append(service)
        if user_impact:
            parts.append(user_impact)
        if business_impact:
            parts.append(business_impact)
        return " ".join(parts).lower()
    
    def _calculate_severity_score(self, text: str) -> float:
        """Calculate score based on keyword severity (0-100)"""
        score = 0
        
        # Check for critical keywords
        for keyword in self.CRITICAL_KEYWORDS:
            if keyword in text:
                score = max(score, 95 + (len(re.findall(keyword, text)) * 2))
        
        # Check for high keywords
        for keyword in self.HIGH_KEYWORDS:
            if keyword in text:
                score = max(score, 70 + (len(re.findall(keyword, text)) * 2))
        
        # Check for medium keywords
        for keyword in self.MEDIUM_KEYWORDS:
            if keyword in text:
                score = max(score, 40 + (len(re.findall(keyword, text)) * 2))
        
        # Check for low keywords
        for keyword in self.LOW_KEYWORDS:
            if keyword in text:
                score = max(score, 10 + (len(re.findall(keyword, text)) * 2))
        
        return min(score, 100)
    
    def _calculate_service_score(self, service: Optional[str]) -> float:
        """Calculate risk based on affected service (0-100)"""
        if not service:
            return 50  # Default if unknown
        
        service = service.lower()
        
        # Critical services
        critical_services = ["payment", "auth", "authentication", "database", "billing"]
        if any(svc in service for svc in critical_services):
            return 90
        
        # High priority services
        high_services = ["api", "gateway", "user", "order", "transaction"]
        if any(svc in service for svc in high_services):
            return 70
        
        # Medium priority
        medium_services = ["notification", "email", "logging", "analytics"]
        if any(svc in service for svc in medium_services):
            return 40
        
        return 30  # Low priority
    
    def _calculate_error_score(self, error_count: Optional[int]) -> float:
        """Calculate score based on error count (0-100)"""
        if error_count is None:
            return 50  # Unknown
        
        if error_count >= 1000:
            return 95
        elif error_count >= 500:
            return 85
        elif error_count >= 100:
            return 70
        elif error_count >= 50:
            return 55
        elif error_count >= 10:
            return 40
        elif error_count > 0:
            return 25
        return 10
    
    def _calculate_impact_score(
        self,
        user_impact: Optional[str],
        business_impact: Optional[str]
    ) -> float:
        """Calculate score based on impact descriptions (0-100)"""
        score = 50  # Default
        
        if user_impact:
            user_impact = user_impact.lower()
            if any(word in user_impact for word in ["all", "complete", "total", "cannot"]):
                score = max(score, 90)
            elif any(word in user_impact for word in ["many", "multiple", "significant"]):
                score = max(score, 70)
            elif any(word in user_impact for word in ["some", "few", "partial"]):
                score = max(score, 40)
        
        if business_impact:
            business_impact = business_impact.lower()
            if any(word in business_impact for word in ["revenue", "money", "loss", "critical"]):
                score = max(score, 95)
            elif any(word in business_impact for word in ["reputation", "customer", "sla"]):
                score = max(score, 75)
        
        return score
    
    def _calculate_timeline_score(self, timeline_events: Optional[List[Dict]]) -> float:
        """Calculate risk based on timeline (0-100)"""
        if not timeline_events:
            return 50  # Unknown
        
        event_count = len(timeline_events)
        
        # More events = higher urgency/complexity
        if event_count >= 20:
            return 85
        elif event_count >= 10:
            return 70
        elif event_count >= 5:
            return 55
        return 40
    
    def _calculate_weighted_score(
        self,
        severity_score: float,
        service_score: float,
        error_score: float,
        impact_score: float,
        timeline_score: float
    ) -> float:
        """Calculate weighted average of all scores"""
        # Weights (total = 1.0)
        weights = {
            "severity": 0.35,    # Highest weight - what happened
            "service": 0.25,     # Service criticality
            "impact": 0.20,      # User/business impact
            "error": 0.15,       # Error count
            "timeline": 0.05     # Timeline complexity
        }
        
        weighted_score = (
            severity_score * weights["severity"] +
            service_score * weights["service"] +
            impact_score * weights["impact"] +
            error_score * weights["error"] +
            timeline_score * weights["timeline"]
        )
        
        return min(weighted_score, 100)
    
    def _determine_severity(self, risk_score: float, text: str) -> str:
        """Determine severity level based on risk score and keywords"""
        # Override based on critical keywords
        for keyword in self.CRITICAL_KEYWORDS[:8]:  # Top critical keywords
            if keyword in text:
                return self.SEVERITY_CRITICAL
        
        # Determine by score
        if risk_score >= 80:
            return self.SEVERITY_CRITICAL
        elif risk_score >= 60:
            return self.SEVERITY_HIGH
        elif risk_score >= 30:
            return self.SEVERITY_MEDIUM
        return self.SEVERITY_LOW
    
    def _calculate_confidence(
        self,
        incident: str,
        logs: Optional[str],
        error_count: Optional[int],
        service: Optional[str],
        timeline: Optional[List[Dict]]
    ) -> float:
        """Calculate confidence in risk assessment (0-100)"""
        confidence = 0
        data_points = 0
        
        # Base confidence from incident description
        if incident and len(incident) > 50:
            confidence += 30
            data_points += 1
        elif incident:
            confidence += 15
            data_points += 1
        
        # Confidence from logs
        if logs and len(logs) > 100:
            confidence += 25
            data_points += 1
        elif logs:
            confidence += 10
            data_points += 1
        
        # Confidence from error count
        if error_count is not None:
            confidence += 15
            data_points += 1
        
        # Confidence from service
        if service:
            confidence += 15
            data_points += 1
        
        # Confidence from timeline
        if timeline and len(timeline) > 3:
            confidence += 15
            data_points += 1
        elif timeline:
            confidence += 5
            data_points += 1
        
        # Adjust based on data completeness
        if data_points >= 4:
            confidence = min(confidence + 10, 100)
        
        return min(confidence, 100)
    
    def _identify_risk_factors(self, text: str) -> List[str]:
        """Identify specific risk factors present"""
        factors = []
        
        # Check for critical factors
        if any(keyword in text for keyword in ["database", "db", "timeout"]):
            factors.append("Database issues detected")
        
        if any(keyword in text for keyword in ["payment", "transaction"]):
            factors.append("Financial transaction affected")
        
        if any(keyword in text for keyword in ["auth", "login", "authentication"]):
            factors.append("Authentication/Authorization issues")
        
        if any(keyword in text for keyword in ["memory", "cpu", "performance"]):
            factors.append("Resource/Performance issues")
        
        if any(keyword in text for keyword in ["outage", "down", "unavailable"]):
            factors.append("Service availability impacted")
        
        if any(keyword in text for keyword in ["error", "failed", "failure"]):
            factors.append("Multiple errors detected")
        
        return factors if factors else ["General incident detected"]
    
    def quick_risk_score(self, incident_description: str, logs: str = "") -> Dict[str, Any]:
        """
        Quick risk assessment (simplified)
        
        Args:
            incident_description: What happened
            logs: Error logs
            
        Returns:
            Dictionary with severity, risk_score, confidence
        """
        return self.calculate_risk(
            incident_description=incident_description,
            logs=logs
        )
