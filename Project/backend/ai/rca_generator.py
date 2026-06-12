"""
RCA Generator
Generates comprehensive Root Cause Analysis reports
"""
from typing import Dict, Any, Optional, List
from loguru import logger

from backend.ai.groq_service import GroqService
from backend.ai.risk_engine import RiskEngine


class RCAGenerator:
    """
    RCA Generator that combines all data sources to generate
    comprehensive Root Cause Analysis reports
    """
    
    def __init__(self):
        """Initialize RCA generator with AI and risk services"""
        self.groq_service = GroqService()
        self.risk_engine = RiskEngine()
        logger.info("RCA Generator initialized")
    
    def generate_rca(
        self,
        incident_description: str,
        github_findings: Optional[Dict[str, Any]] = None,
        log_findings: Optional[Dict[str, Any]] = None,
        timeline: Optional[Dict[str, Any]] = None,
        affected_service: Optional[str] = None,
        similar_incidents: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive RCA from all available data
        
        Args:
            incident_description: What happened
            github_findings: Analysis from GitHub commits
            log_findings: Analysis from logs
            timeline: Timeline of events
            affected_service: Service affected
            similar_incidents: Similar past incidents (optional)
            
        Returns:
            Complete RCA with root cause, impact, recommendations, prevention
        """
        logger.info("Generating comprehensive RCA")
        
        try:
            # Step 1: Calculate risk score
            risk_data = self._calculate_risk(
                incident_description=incident_description,
                log_findings=log_findings,
                affected_service=affected_service,
                timeline=timeline
            )
            
            # Step 2: Identify root cause candidates
            root_cause_candidates = self._identify_root_causes(
                github_findings=github_findings,
                log_findings=log_findings,
                timeline=timeline
            )
            
            # Step 3: Generate RCA using Groq
            rca_result = self.groq_service.generate_rca(
                incident_description=incident_description,
                severity=risk_data["severity"],
                affected_service=affected_service or "unknown",
                risk_score=risk_data["risk_score"],
                github_analysis=github_findings or {},
                log_analysis=log_findings or {},
                timeline=timeline or {},
                root_cause_candidates=root_cause_candidates,
                similar_incidents=similar_incidents
            )
            
            # Step 4: Compile complete RCA
            complete_rca = {
                "success": rca_result.get("success", False),
                "rca_text": rca_result.get("rca_text", ""),
                "risk_assessment": risk_data,
                "root_cause_candidates": root_cause_candidates,
                "model_used": rca_result.get("model_used"),
                "metadata": {
                    "incident": incident_description,
                    "severity": risk_data["severity"],
                    "risk_score": risk_data["risk_score"],
                    "confidence": risk_data["confidence"],
                    "affected_service": affected_service
                }
            }
            
            logger.info("RCA generated successfully")
            return complete_rca
            
        except Exception as e:
            logger.error(f"Error generating RCA: {e}")
            return {
                "success": False,
                "error": str(e),
                "rca_text": f"Error generating RCA: {str(e)}"
            }
    
    def generate_quick_rca(
        self,
        incident_description: str,
        logs: str,
        timeline: str
    ) -> Dict[str, Any]:
        """
        Generate quick RCA for fast triage
        
        Args:
            incident_description: What happened
            logs: Log summary
            timeline: Timeline summary
            
        Returns:
            Quick RCA analysis
        """
        logger.info("Generating quick RCA")
        
        try:
            # Quick risk assessment
            risk_data = self.risk_engine.quick_risk_score(
                incident_description=incident_description,
                logs=logs
            )
            
            # Quick RCA from Groq
            rca_result = self.groq_service.generate_quick_rca(
                incident_description=incident_description,
                log_summary=logs,
                timeline_summary=timeline
            )
            
            return {
                "success": rca_result.get("success", False),
                "rca_text": rca_result.get("rca_text", ""),
                "risk_assessment": risk_data,
                "metadata": {
                    "incident": incident_description,
                    "severity": risk_data["severity"],
                    "risk_score": risk_data["risk_score"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating quick RCA: {e}")
            return {
                "success": False,
                "error": str(e),
                "rca_text": f"Error: {str(e)}"
            }
    
    def _calculate_risk(
        self,
        incident_description: str,
        log_findings: Optional[Dict[str, Any]],
        affected_service: Optional[str],
        timeline: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate risk assessment"""
        
        # Extract log summary
        log_summary = ""
        error_count = None
        if log_findings:
            log_summary = log_findings.get("summary", "")
            error_count = log_findings.get("error_count")
        
        # Extract timeline events
        timeline_events = None
        if timeline:
            timeline_events = timeline.get("events", [])
        
        return self.risk_engine.calculate_risk(
            incident_description=incident_description,
            logs=log_summary,
            affected_service=affected_service,
            error_count=error_count,
            timeline_events=timeline_events
        )
    
    def _identify_root_causes(
        self,
        github_findings: Optional[Dict[str, Any]],
        log_findings: Optional[Dict[str, Any]],
        timeline: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identify potential root cause candidates
        
        Returns:
            List of root cause candidates with confidence scores
        """
        candidates = []
        
        # Analyze GitHub changes
        if github_findings and github_findings.get("commits"):
            commits = github_findings.get("commits", [])
            if commits:
                # Recent config/deployment changes are high confidence
                for commit in commits[:3]:  # Top 3 recent commits
                    message = commit.get("message", "").lower()
                    files = commit.get("changed_files", [])
                    
                    confidence = 0.5  # Base confidence
                    
                    # Higher confidence for config changes
                    if any(word in message for word in ["config", "setting", "parameter"]):
                        confidence = 0.85
                    elif any(word in message for word in ["deploy", "release", "update"]):
                        confidence = 0.75
                    elif any(word in message for word in ["fix", "patch", "hotfix"]):
                        confidence = 0.65
                    
                    # Check changed files
                    config_files = ["config", "settings", ".env", "yaml", "yml", "json"]
                    if any(cf in str(files).lower() for cf in config_files):
                        confidence = max(confidence, 0.80)
                    
                    candidates.append({
                        "type": "code_change",
                        "confidence": confidence,
                        "description": f"Recent commit: {commit.get('message', 'Unknown')}",
                        "details": {
                            "commit_sha": commit.get("sha", ""),
                            "changed_files": files[:5]  # Top 5 files
                        }
                    })
        
        # Analyze log patterns
        if log_findings:
            error_patterns = log_findings.get("error_patterns", {})
            critical_errors = log_findings.get("critical_errors", [])
            
            # High frequency errors are likely causes
            if error_patterns:
                for pattern, count in list(error_patterns.items())[:3]:
                    confidence = min(0.9, 0.6 + (count / 100))  # Higher count = higher confidence
                    candidates.append({
                        "type": "error_pattern",
                        "confidence": confidence,
                        "description": f"Frequent error pattern: {pattern} (occurred {count} times)",
                        "details": {
                            "pattern": pattern,
                            "count": count
                        }
                    })
            
            # Critical errors
            if critical_errors:
                for error in critical_errors[:2]:
                    candidates.append({
                        "type": "critical_error",
                        "confidence": 0.85,
                        "description": f"Critical error: {error.get('message', 'Unknown')}",
                        "details": error
                    })
        
        # Analyze timeline for patterns
        if timeline and timeline.get("events"):
            events = timeline.get("events", [])
            
            # Look for deployment -> error pattern
            deployment_events = [e for e in events if e.get("event_type") == "deployment"]
            error_events = [e for e in events if e.get("event_type") == "error"]
            
            if deployment_events and error_events:
                # Check if errors started after deployment
                last_deploy = deployment_events[-1] if deployment_events else None
                first_error = error_events[0] if error_events else None
                
                if last_deploy and first_error:
                    candidates.append({
                        "type": "deployment_correlation",
                        "confidence": 0.90,
                        "description": f"Errors started after deployment at {last_deploy.get('timestamp')}",
                        "details": {
                            "deployment_time": last_deploy.get("timestamp"),
                            "first_error_time": first_error.get("timestamp"),
                            "error_description": first_error.get("description")
                        }
                    })
        
        # Sort by confidence
        candidates.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return top 5 candidates
        return candidates[:5] if candidates else [{
            "type": "unknown",
            "confidence": 0.3,
            "description": "Root cause requires further investigation",
            "details": {}
        }]
