"""
Member 1 Integration Service
Consumes APIs from Member 1 (Investigation Backend) to get real investigation data
"""
from typing import Dict, Any, Optional
import requests
from loguru import logger

from backend.ai.config import settings


class Member1IntegrationService:
    """
    Service for integrating with Member 1 (Investigation Backend)
    
    Consumes:
    - GET /investigations/{id} - Get investigation data
    - GET /timeline/{id} - Get timeline data
    
    Receives:
    - GitHub Findings
    - Render Logs
    - Timeline
    - Severity
    
    Feeds into:
    - RCA Engine
    - Risk Engine
    - RAG System
    """
    
    def __init__(self):
        """Initialize Member 1 integration service"""
        self.base_url = settings.INVESTIGATION_BACKEND_URL
        logger.info(f"Member 1 Integration initialized: {self.base_url}")
    
    def get_investigation(self, investigation_id: int) -> Dict[str, Any]:
        """
        Get complete investigation data from Member 1
        
        Args:
            investigation_id: Investigation ID
            
        Returns:
            Investigation data with GitHub, logs, timeline, severity
            
        Raises:
            ConnectionError: If Member 1 is not available
            ValueError: If investigation not found
        """
        try:
            logger.info(f"Fetching investigation {investigation_id} from Member 1")
            
            url = f"{self.base_url}/investigations/{investigation_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                raise ValueError(f"Investigation {investigation_id} not found")
            
            if response.status_code != 200:
                raise ConnectionError(f"Member 1 returned status {response.status_code}")
            
            data = response.json()
            
            logger.info(f"✅ Investigation {investigation_id} retrieved successfully")
            logger.debug(f"Investigation data: {data}")
            
            return data
            
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Member 1 (Investigation Backend)")
            logger.error(f"URL: {url}")
            raise ConnectionError(
                f"Member 1 (Investigation Backend) is not available at {self.base_url}. "
                "Make sure it's running on http://localhost:8000"
            )
        except requests.exceptions.Timeout:
            logger.error("❌ Request to Member 1 timed out")
            raise ConnectionError("Member 1 request timed out")
        except Exception as e:
            logger.error(f"❌ Error getting investigation: {e}")
            raise
    
    def get_timeline(self, investigation_id: int) -> Dict[str, Any]:
        """
        Get timeline data from Member 1
        
        Args:
            investigation_id: Investigation ID
            
        Returns:
            Timeline data with events
        """
        try:
            logger.info(f"Fetching timeline for investigation {investigation_id}")
            
            url = f"{self.base_url}/timeline/{investigation_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                raise ValueError(f"Timeline for investigation {investigation_id} not found")
            
            if response.status_code != 200:
                raise ConnectionError(f"Member 1 returned status {response.status_code}")
            
            data = response.json()
            
            logger.info(f"✅ Timeline retrieved successfully")
            logger.debug(f"Timeline data: {data}")
            
            return data
            
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Member 1")
            raise ConnectionError(
                f"Member 1 is not available at {self.base_url}"
            )
        except Exception as e:
            logger.error(f"❌ Error getting timeline: {e}")
            raise
    
    def extract_for_rca(self, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data for RCA Engine
        
        Args:
            investigation_data: Raw investigation data from Member 1
            
        Returns:
            Formatted data for RCA generation
        """
        try:
            # Extract core incident info
            incident_description = investigation_data.get('incident_description', '')
            severity = investigation_data.get('severity', 'medium')
            
            # Extract investigation results
            investigation = investigation_data.get('investigation', {})
            
            # Extract GitHub findings
            github_analysis = investigation_data.get('github_analysis', {})
            
            # Extract log analysis
            log_analysis = investigation_data.get('log_analysis', {})
            
            # Build RCA input
            rca_input = {
                "incident": incident_description,
                "severity": severity.lower() if severity else "medium",
                "affected_service": "investigation",
                "github_analysis": github_analysis,
                "log_analysis": log_analysis,
                "timeline": investigation.get('timeline', []),
                "root_cause_candidates": [investigation.get('probable_root_cause', {})]
            }
            
            logger.info("✅ Data extracted for RCA Engine")
            return rca_input
            
        except Exception as e:
            logger.error(f"❌ Error extracting RCA data: {e}")
            # Return minimal data for graceful handling
            return {
                "incident": investigation_data.get('incident_description', 'Unknown incident'),
                "severity": "medium",
                "affected_service": "investigation"
            }
    
    def extract_for_risk_engine(self, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data for Risk Engine
        
        Args:
            investigation_data: Raw investigation data from Member 1
            
        Returns:
            Formatted data for risk scoring
        """
        try:
            investigation = investigation_data.get('investigation', {})
            log_analysis = investigation_data.get('log_analysis', {})
            
            risk_input = {
                "incident_description": investigation_data.get('incident_description', ''),
                "severity": investigation_data.get('severity', 'medium'),
                "affected_service": "investigation",
                "error_count": log_analysis.get('error_count', 0),
                "log_source": log_analysis.get('source', 'unknown'),
                "incident_type": investigation.get('incident_type', 'Unknown'),
                "timeline": investigation.get('timeline', [])
            }
            
            logger.info("✅ Data extracted for Risk Engine")
            return risk_input
            
        except Exception as e:
            logger.error(f"❌ Error extracting risk data: {e}")
            return {
                "incident_description": investigation_data.get('incident_description', 'Unknown'),
                "severity": "medium",
                "affected_service": "investigation"
            }
    
    def extract_for_rag(self, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant data for RAG System
        
        Args:
            investigation_data: Raw investigation data from Member 1
            
        Returns:
            Formatted data for RAG retrieval
        """
        try:
            investigation = investigation_data.get('investigation', {})
            
            rag_input = {
                "incident_description": investigation_data.get('incident_description', ''),
                "incident_type": investigation.get('incident_type', 'Unknown'),
                "severity": investigation_data.get('severity', 'medium'),
                "root_cause": investigation.get('probable_root_cause', {}).get('description', ''),
                "keywords": [
                    investigation_data.get('incident_description', ''),
                    investigation.get('incident_type', ''),
                    investigation.get('probable_root_cause', {}).get('description', '')
                ]
            }
            
            logger.info("✅ Data extracted for RAG System")
            return rag_input
            
        except Exception as e:
            logger.error(f"❌ Error extracting RAG data: {e}")
            return {
                "incident_description": investigation_data.get('incident_description', 'Unknown'),
                "keywords": []
            }
    
    def process_investigation_full(
        self, 
        investigation_id: int,
        generate_rca: bool = True,
        calculate_risk: bool = True,
        find_similar: bool = True
    ) -> Dict[str, Any]:
        """
        Full processing pipeline: Get data from Member 1 and process through all engines
        
        Args:
            investigation_id: Investigation ID
            generate_rca: Generate RCA using Groq
            calculate_risk: Calculate risk score
            find_similar: Find similar incidents using RAG
            
        Returns:
            Complete processing results
        """
        try:
            logger.info(f"Starting full processing for investigation {investigation_id}")
            
            # Step 1: Get investigation data from Member 1
            investigation_data = self.get_investigation(investigation_id)
            
            # Step 2: Get timeline data
            try:
                timeline_data = self.get_timeline(investigation_id)
                investigation_data['timeline_data'] = timeline_data
            except Exception as e:
                logger.warning(f"Could not get timeline: {e}")
                investigation_data['timeline_data'] = {"timeline": []}
            
            results = {
                "investigation_id": investigation_id,
                "raw_data": investigation_data,
                "processing": {}
            }
            
            # Step 3: Extract for RCA Engine (if requested)
            if generate_rca:
                rca_input = self.extract_for_rca(investigation_data)
                results['processing']['rca_input'] = rca_input
            
            # Step 4: Extract for Risk Engine (if requested)
            if calculate_risk:
                risk_input = self.extract_for_risk_engine(investigation_data)
                results['processing']['risk_input'] = risk_input
            
            # Step 5: Extract for RAG (if requested)
            if find_similar:
                rag_input = self.extract_for_rag(investigation_data)
                results['processing']['rag_input'] = rag_input
            
            logger.info(f"✅ Full processing completed for investigation {investigation_id}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in full processing: {e}")
            raise
    
    def check_member1_health(self) -> Dict[str, Any]:
        """
        Check if Member 1 is available
        
        Returns:
            Health status
        """
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "available": True,
                    "url": self.base_url,
                    "response": response.json()
                }
            else:
                return {
                    "status": "unhealthy",
                    "available": False,
                    "url": self.base_url,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "status": "unavailable",
                "available": False,
                "url": self.base_url,
                "error": str(e)
            }
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "service": "Member 1 Integration",
            "description": "Consumes investigation data from Member 1 (Investigation Backend)",
            "base_url": self.base_url,
            "endpoints_consumed": [
                "GET /investigations/{id}",
                "GET /timeline/{id}",
                "GET /health"
            ],
            "data_received": [
                "GitHub Findings",
                "Render Logs",
                "Timeline",
                "Severity",
                "Investigation Results"
            ],
            "feeds_into": [
                "RCA Engine (Groq AI)",
                "Risk Engine (Multi-factor scoring)",
                "RAG System (Similar incidents)"
            ]
        }
