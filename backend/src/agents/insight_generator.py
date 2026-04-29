"""Insight Generator Agent - Extracts deeper insights and patterns"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from ..config import config


@dataclass
class Insights:
    """Structured insights output"""
    patterns: List[str]  # Key patterns identified
    implications: List[str]  # Implications of the content
    action_items: List[str]  # Actionable items
    related_topics: List[str]  # Related areas to explore
    questions: List[str]  # Follow-up questions


class InsightGenerator:
    """Generates deeper insights using Ollama"""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize insight generator"""
        self.model = model or config.OLLAMA_MODEL
        self.base_url = config.OLLAMA_BASE_URL
    
    def generate_insights(self, transcript_text: str, summary: str) -> Insights:
        """
        Generate deeper insights from transcript and summary
        
        Args:
            transcript_text: Full transcript text
            summary: Previously generated summary
            
        Returns:
            Insights object with structured output
        """
        patterns = self._identify_patterns(transcript_text)
        implications = self._generate_implications(transcript_text, summary)
        action_items = self._generate_action_items(transcript_text, summary)
        related_topics = self._suggest_related_topics(transcript_text)
        questions = self._generate_follow_up_questions(transcript_text, summary)
        
        return Insights(
            patterns=patterns,
            implications=implications,
            action_items=action_items,
            related_topics=related_topics,
            questions=questions,
        )
    
    def _identify_patterns(self, transcript_text: str) -> List[str]:
        """Identify key patterns in the content"""
        prompt = f"""Identify 3-4 key patterns or recurring themes in this transcript.
Each pattern should be concise and specific.
Return patterns one per line without numbering.

Transcript:
{transcript_text[:2000]}

Patterns:"""
        
        response = self._call_ollama(prompt).strip()
        patterns = [line.strip() for line in response.split("\n") if line.strip()]
        return patterns[:4]
    
    def _generate_implications(self, transcript_text: str, summary: str) -> List[str]:
        """Generate implications of the content"""
        prompt = f"""Based on this content, what are the key implications or consequences?
List 2-3 important implications.
Return one per line without numbering.

Summary: {summary}

Transcript: {transcript_text[:1500]}

Implications:"""
        
        response = self._call_ollama(prompt).strip()
        implications = [line.strip() for line in response.split("\n") if line.strip()]
        return implications[:3]
    
    def _generate_action_items(self, transcript_text: str, summary: str) -> List[str]:
        """Generate actionable items based on content"""
        prompt = f"""What are 3-4 actionable items or recommendations based on this content?
Each should be specific and implementable.
Return one per line without numbering.

Summary: {summary}

Transcript: {transcript_text[:1500]}

Action Items:"""
        
        response = self._call_ollama(prompt).strip()
        action_items = [line.strip() for line in response.split("\n") if line.strip()]
        return action_items[:4]
    
    def _suggest_related_topics(self, transcript_text: str) -> List[str]:
        """Suggest related topics to explore further"""
        prompt = f"""What are 3-4 related topics that would complement understanding of this content?
Topics should build on or extend the concepts discussed.
Return one per line without numbering.

Transcript: {transcript_text[:1500]}

Related Topics:"""
        
        response = self._call_ollama(prompt).strip()
        topics = [line.strip() for line in response.split("\n") if line.strip()]
        return topics[:4]
    
    def _generate_follow_up_questions(self, transcript_text: str, summary: str) -> List[str]:
        """Generate follow-up questions for deeper exploration"""
        prompt = f"""Generate 3 thoughtful follow-up questions that would deepen understanding of this topic.
Questions should be open-ended and thought-provoking.
Return one per line without numbering.

Summary: {summary}

Transcript: {transcript_text[:1500]}

Follow-up Questions:"""
        
        response = self._call_ollama(prompt).strip()
        questions = [line.strip() for line in response.split("\n") if line.strip()]
        return questions[:3]
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API to generate response"""
        try:
            import requests
        except ImportError:
            raise ImportError("requests not installed. Install with: pip install requests")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": config.TEMPERATURE,
                    "num_predict": config.MAX_TOKENS,
                },
                timeout=config.OLLAMA_TIMEOUT,
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                raise RuntimeError(f"Ollama error: {response.status_code}")
        
        except Exception as e:
            raise RuntimeError(f"Failed to call Ollama: {str(e)}")
