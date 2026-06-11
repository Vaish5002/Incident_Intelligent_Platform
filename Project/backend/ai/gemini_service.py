"""
Gemini AI Service
Handles all interactions with Google Gemini API
"""
import google.generativeai as genai
from typing import Dict, Any, Optional
from loguru import logger

from backend.ai.config import settings
from backend.ai.prompts import (
    build_rca_prompt,
    build_quick_rca_prompt,
    RECOMMENDATION_PROMPT,
    SIMILAR_INCIDENT_ANALYSIS_PROMPT,
    PREVENTION_STRATEGY_PROMPT
)


class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini service"""
        self.api_key = api_key or settings.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.model_name = settings.GEMINI_MODEL
        
        # Generation config
        self.generation_config = {
            "temperature": settings.TEMPERATURE,
            "max_output_tokens": settings.MAX_TOKENS,
        }
        
        logger.info(f"Gemini service initialized with model: {settings.GEMINI_MODEL}")
    
    def generate_text(self, prompt: str) -> Dict[str, Any]:
        """
        Generate text using Gemini (generic method)
        
        Args:
            prompt: Text prompt
            
        Returns:
            Dictionary with generated text
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "success": True,
                "text": response.text
            }
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_rca(
        self,
        incident_description: str,
        severity: str,
        affected_service: str,
        risk_score: float,
        github_analysis: Dict[str, Any],
        log_analysis: Dict[str, Any],
        timeline: Dict[str, Any],
        root_cause_candidates: list,
        similar_incidents: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive Root Cause Analysis using Gemini
        
        Args:
            incident_description: Description of the incident
            severity: Incident severity (low/medium/high/critical)
            affected_service: Service affected by incident
            risk_score: Risk score (0-100)
            github_analysis: GitHub analysis data
            log_analysis: Log analysis data
            timeline: Timeline of events
            root_cause_candidates: Pre-analyzed root cause candidates
            similar_incidents: Similar past incidents (optional)
            
        Returns:
            Dictionary containing generated RCA
        """
        try:
            logger.info("Generating RCA with Gemini")
            
            # Format data for prompt
            github_text = self._format_github_analysis(github_analysis)
            log_text = self._format_log_analysis(log_analysis)
            timeline_text = self._format_timeline(timeline)
            candidates_text = self._format_root_cause_candidates(root_cause_candidates)
            similar_text = similar_incidents or "No similar incidents found in history."
            
            # Build prompt
            prompt = build_rca_prompt(
                incident_description=incident_description,
                severity=severity,
                affected_service=affected_service,
                risk_score=risk_score,
                github_analysis=github_text,
                log_analysis=log_text,
                timeline=timeline_text,
                root_cause_candidates=candidates_text,
                similar_incidents=similar_text
            )
            
            # Generate RCA
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            rca_text = response.text
            
            logger.info("RCA generated successfully")
            
            return {
                "rca_text": rca_text,
                "model_used": settings.GEMINI_MODEL,
                "prompt_tokens": len(prompt.split()),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating RCA: {e}")
            return {
                "rca_text": f"Error generating RCA: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def generate_quick_rca(
        self,
        incident_description: str,
        log_summary: str,
        timeline_summary: str
    ) -> Dict[str, Any]:
        """Generate quick RCA for fast analysis"""
        
        try:
            logger.info("Generating quick RCA")
            
            prompt = build_quick_rca_prompt(
                incident_description=incident_description,
                log_summary=log_summary,
                timeline_summary=timeline_summary
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "rca_text": response.text,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating quick RCA: {e}")
            return {
                "rca_text": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def generate_recommendations(
        self,
        root_cause: str,
        severity: str,
        affected_service: str
    ) -> Dict[str, Any]:
        """Generate actionable recommendations"""
        
        try:
            logger.info("Generating recommendations")
            
            prompt = RECOMMENDATION_PROMPT.format(
                root_cause=root_cause,
                severity=severity,
                affected_service=affected_service
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "recommendations": response.text,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                "recommendations": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def analyze_similar_incidents(
        self,
        current_incident: str,
        past_incidents: list
    ) -> Dict[str, Any]:
        """Analyze patterns from similar past incidents"""
        
        try:
            logger.info("Analyzing similar incidents")
            
            # Format past incidents
            past_incidents_text = "\n\n".join([
                f"**Incident {i+1}:**\n{incident}"
                for i, incident in enumerate(past_incidents)
            ])
            
            prompt = SIMILAR_INCIDENT_ANALYSIS_PROMPT.format(
                current_incident=current_incident,
                past_incidents=past_incidents_text
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "analysis": response.text,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error analyzing similar incidents: {e}")
            return {
                "analysis": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def generate_prevention_strategy(
        self,
        root_cause: str,
        affected_service: str,
        risk_score: float
    ) -> Dict[str, Any]:
        """Generate prevention strategy"""
        
        try:
            logger.info("Generating prevention strategy")
            
            prompt = PREVENTION_STRATEGY_PROMPT.format(
                root_cause=root_cause,
                affected_service=affected_service,
                risk_score=risk_score
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "prevention_strategy": response.text,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating prevention strategy: {e}")
            return {
                "prevention_strategy": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    # Helper methods for formatting data
    
    def _format_github_analysis(self, github_data: Dict) -> str:
        """Format GitHub analysis for prompt"""
        
        if not github_data:
            return "No GitHub data available."
        
        parts = [
            f"**Repository:** {github_data.get('repo_name', 'Unknown')}",
            f"**Recent Commits:** {github_data.get('total_commits', 0)}",
        ]
        
        commits = github_data.get('commits', [])
        if commits:
            parts.append("\n**Recent Changes:**")
            for commit in commits[:5]:  # Top 5 commits
                parts.append(f"- {commit.get('sha', '')}: {commit.get('message', '')}")
        
        changed_files = github_data.get('changed_files', [])
        if changed_files:
            parts.append(f"\n**Files Modified:** {', '.join(changed_files[:10])}")
        
        return "\n".join(parts)
    
    def _format_log_analysis(self, log_data: Dict) -> str:
        """Format log analysis for prompt"""
        
        if not log_data:
            return "No log data available."
        
        parts = [
            f"**Total Logs:** {log_data.get('total_logs', 0)}",
            f"**Errors:** {log_data.get('error_count', 0)}",
            f"**Warnings:** {log_data.get('warning_count', 0)}",
        ]
        
        critical_errors = log_data.get('critical_errors', [])
        if critical_errors:
            parts.append("\n**Critical Errors:**")
            for error in critical_errors[:5]:  # Top 5 errors
                parts.append(f"- [{error.get('timestamp', '')}] {error.get('message', '')}")
        
        error_patterns = log_data.get('error_patterns', {})
        if error_patterns:
            patterns = ", ".join([f"{k} ({v})" for k, v in list(error_patterns.items())[:5]])
            parts.append(f"\n**Error Patterns:** {patterns}")
        
        return "\n".join(parts)
    
    def _format_timeline(self, timeline_data: Dict) -> str:
        """Format timeline for prompt"""
        
        if not timeline_data:
            return "No timeline data available."
        
        events = timeline_data.get('events', [])
        if not events:
            return "No events in timeline."
        
        parts = ["**Chronological Events:**"]
        for event in events[:15]:  # Top 15 events
            event_type = event.get('event_type', 'unknown').upper()
            timestamp = event.get('timestamp', '')
            description = event.get('description', '')
            parts.append(f"- [{timestamp}] {event_type}: {description}")
        
        return "\n".join(parts)
    
    def _format_root_cause_candidates(self, candidates: list) -> str:
        """Format root cause candidates for prompt"""
        
        if not candidates:
            return "No root cause candidates identified."
        
        parts = ["**Pre-analyzed Root Cause Candidates:**"]
        for i, candidate in enumerate(candidates, 1):
            confidence = candidate.get('confidence', 0) * 100
            parts.append(
                f"{i}. [{confidence:.0f}% confidence] {candidate.get('description', 'Unknown')}"
            )
        
        return "\n".join(parts)
