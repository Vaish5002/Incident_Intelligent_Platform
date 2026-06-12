"""
AI Copilot Service
Interactive incident assistant powered by Groq
"""
from typing import Dict, Any, Optional, List
from loguru import logger

from backend.ai.groq_service import GroqService
from backend.ai.rag_service import RAGService


class CopilotService:
    """
    AI Copilot - Interactive assistant for incident investigation
    
    Answers questions like:
    - Why did this happen?
    - Which commit caused this?
    - How do we prevent this?
    - What should we do next?
    """
    
    def __init__(self):
        """Initialize copilot service"""
        self.groq = GroqService()
        self.rag = RAGService()
        self.conversation_history: List[Dict[str, str]] = []
        logger.info("AI Copilot initialized")
    
    def ask(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None,
        use_history: bool = True
    ) -> Dict[str, Any]:
        """
        Ask the AI Copilot a question
        
        Args:
            question: User's question
            context: Incident context (RCA, logs, GitHub data, etc.)
            use_history: Whether to use conversation history
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Validate question
            if not question or not question.strip():
                return {
                    "success": False,
                    "error": "Question cannot be empty",
                    "answer": "Please provide a question."
                }
            
            # Build context prompt
            context_parts = []
            
            # Add incident context if provided
            if context:
                context_parts.append("## Incident Context\n")
                
                if context.get("incident"):
                    context_parts.append(f"**Incident:** {context['incident']}\n")
                
                if context.get("severity"):
                    context_parts.append(f"**Severity:** {context['severity']}\n")
                
                if context.get("affected_service"):
                    context_parts.append(f"**Affected Service:** {context['affected_service']}\n")
                
                if context.get("rca_text"):
                    context_parts.append(f"\n**Root Cause Analysis:**\n{context['rca_text'][:1000]}...\n")
                
                if context.get("logs"):
                    context_parts.append(f"\n**Recent Logs:**\n{context['logs'][:500]}...\n")
                
                if context.get("github_analysis"):
                    github = context["github_analysis"]
                    if github.get("commits"):
                        context_parts.append(f"\n**Recent Commits:** {len(github['commits'])} commits\n")
                        for commit in github["commits"][:3]:
                            context_parts.append(f"- {commit.get('message', 'N/A')}\n")
                
                if context.get("timeline"):
                    context_parts.append(f"\n**Timeline:** {context['timeline']}\n")
                
                if context.get("recommendations"):
                    context_parts.append(f"\n**Recommendations:** {context['recommendations'][:500]}...\n")
            
            # Add conversation history if enabled
            if use_history and self.conversation_history:
                context_parts.append("\n## Previous Conversation\n")
                for entry in self.conversation_history[-3:]:  # Last 3 exchanges
                    context_parts.append(f"**User:** {entry['question']}\n")
                    context_parts.append(f"**Assistant:** {entry['answer'][:200]}...\n")
            
            context_text = "\n".join(context_parts)
            
            # Build copilot prompt
            prompt = self._build_copilot_prompt(question, context_text)
            
            # Get answer from Groq
            logger.info(f"Copilot question: {question}")
            response = self.groq.generate_text(prompt)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": response.get("error", "Failed to generate response"),
                    "answer": "I apologize, but I'm having trouble generating a response right now."
                }
            
            answer = response["text"]
            
            # Store in conversation history
            if use_history:
                self.conversation_history.append({
                    "question": question,
                    "answer": answer
                })
            
            # Detect question type
            question_type = self._detect_question_type(question)
            
            logger.info(f"Copilot answered ({question_type}): {answer[:100]}...")
            
            return {
                "success": True,
                "answer": answer,
                "question": question,
                "question_type": question_type,
                "used_context": bool(context),
                "used_history": use_history and len(self.conversation_history) > 1
            }
            
        except Exception as e:
            logger.error(f"Error in copilot ask: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "answer": "I encountered an error processing your question. Please try again."
            }
    
    def _build_copilot_prompt(self, question: str, context: str) -> str:
        """
        Build prompt for copilot
        
        Args:
            question: User's question
            context: Context information
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are an AI Copilot assisting with incident investigation and root cause analysis.

You have access to incident context including RCA reports, logs, GitHub commits, and historical data.

Your role is to:
1. Answer questions clearly and concisely
2. Use the provided context to give accurate answers
3. Provide actionable insights when possible
4. Admit when you don't have enough information
5. Suggest next steps when appropriate

## Available Context

{context if context else "No specific context available."}

## User Question

{question}

## Instructions

- Answer the user's question directly and clearly
- Reference specific details from the context when available
- If the context doesn't contain the answer, say so honestly
- Keep answers concise but informative (2-4 paragraphs max)
- Use bullet points for lists and action items
- Be professional but conversational

## Your Answer
"""
        return prompt
    
    def _detect_question_type(self, question: str) -> str:
        """
        Detect the type of question
        
        Args:
            question: User's question
            
        Returns:
            Question type category
        """
        question_lower = question.lower()
        
        # Why questions
        if any(word in question_lower for word in ["why", "what caused", "root cause"]):
            return "causality"
        
        # How to prevent
        if any(word in question_lower for word in ["prevent", "avoid", "stop"]):
            return "prevention"
        
        # What to do
        if any(word in question_lower for word in ["what should", "what do", "next step", "how to fix"]):
            return "action"
        
        # Which commit/change
        if any(word in question_lower for word in ["which commit", "which change", "what changed"]):
            return "investigation"
        
        # When questions
        if any(word in question_lower for word in ["when", "timeline", "how long"]):
            return "timeline"
        
        # Who questions
        if any(word in question_lower for word in ["who", "whose"]):
            return "attribution"
        
        # General
        return "general"
    
    def explain_rca(
        self,
        rca_text: str,
        focus: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Explain an RCA in simpler terms
        
        Args:
            rca_text: Full RCA text
            focus: Optional focus area (root_cause, impact, recommendations, prevention)
            
        Returns:
            Simplified explanation
        """
        if focus:
            question = f"Explain the {focus} section of this RCA in simple terms"
        else:
            question = "Explain this RCA in simple terms for someone non-technical"
        
        return self.ask(
            question=question,
            context={"rca_text": rca_text},
            use_history=False
        )
    
    def suggest_next_steps(
        self,
        incident: str,
        current_status: str,
        actions_taken: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Suggest next steps for incident resolution
        
        Args:
            incident: Incident description
            current_status: Current investigation status
            actions_taken: List of actions already taken
            
        Returns:
            Suggested next steps
        """
        context = {
            "incident": incident,
            "current_status": current_status
        }
        
        if actions_taken:
            context["actions_taken"] = "\n".join(f"- {action}" for action in actions_taken)
        
        return self.ask(
            question="What should we do next to resolve this incident?",
            context=context,
            use_history=False
        )
    
    def compare_with_similar(
        self,
        current_incident: str,
        logs: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find and compare with similar historical incidents
        
        Args:
            current_incident: Current incident description
            logs: Optional logs
            
        Returns:
            Comparison and insights
        """
        # Get similar incidents from RAG
        similar = self.rag.find_similar_incidents(
            incident_description=current_incident,
            logs=logs,
            top_k=3
        )
        
        if not similar["success"] or not similar["similar_incidents"]:
            return {
                "success": True,
                "answer": "No similar historical incidents found in the database.",
                "similar_incidents": []
            }
        
        # Build context with similar incidents
        context = {
            "incident": current_incident,
            "logs": logs
        }
        
        similar_text_parts = []
        for inc in similar["similar_incidents"]:
            similar_text_parts.append(f"\n**Similar Incident ({inc['similarity']}% match):**")
            similar_text_parts.append(f"- Description: {inc['description']}")
            similar_text_parts.append(f"- Severity: {inc['severity']}")
            if inc.get("rca_summary"):
                similar_text_parts.append(f"- Root Cause: {inc['rca_summary'].get('root_cause', 'N/A')[:200]}")
        
        context["similar_incidents"] = "\n".join(similar_text_parts)
        
        response = self.ask(
            question="Based on these similar past incidents, what insights can you provide about the current incident?",
            context=context,
            use_history=False
        )
        
        response["similar_incidents"] = similar["similar_incidents"]
        return response
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history
        
        Returns:
            List of question-answer pairs
        """
        return self.conversation_history.copy()
    
    def get_suggested_questions(
        self,
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Get suggested questions based on context
        
        Args:
            context: Incident context
            
        Returns:
            List of suggested questions
        """
        suggestions = [
            "Why did this incident happen?",
            "What should we do next?",
            "How can we prevent this in the future?",
        ]
        
        if context:
            if context.get("github_analysis"):
                suggestions.append("Which commit might have caused this issue?")
            
            if context.get("logs"):
                suggestions.append("What do the error logs tell us?")
            
            if context.get("rca_text"):
                suggestions.append("Explain the root cause in simple terms")
            
            if context.get("severity") in ["Critical", "High"]:
                suggestions.append("What are the immediate actions we should take?")
        
        return suggestions
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get copilot service information
        
        Returns:
            Service metadata
        """
        return {
            "service": "AI Copilot",
            "status": "operational",
            "ai_model": self.groq.model_name,
            "conversation_history_size": len(self.conversation_history),
            "capabilities": [
                "Answer incident questions",
                "Explain RCA reports",
                "Suggest next steps",
                "Compare with similar incidents",
                "Context-aware responses"
            ],
            "supported_questions": [
                "Why did this happen?",
                "Which commit caused this?",
                "How do we prevent this?",
                "What should we do next?",
                "Explain the root cause",
                "What do the logs tell us?"
            ]
        }
