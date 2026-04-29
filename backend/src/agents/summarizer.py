"""Content Summarizer Agent - Generates summaries and key points from transcripts"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from ..config import config


@dataclass
class Summary:
    """Structured summary output"""
    short_summary: str  # 2-3 sentences
    bullet_points: List[str]  # 5-7 key points
    key_takeaways: List[str]  # Top 3 takeaways
    topics: List[str]  # Main topics covered


class ContentSummarizer:
    """Generates summaries using Ollama"""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize summarizer"""
        self.model = model or config.OLLAMA_MODEL
        self.base_url = config.OLLAMA_BASE_URL
    
    def summarize(self, transcript_text: str) -> Summary:
        """
        Generate structured summary from transcript
        
        Args:
            transcript_text: Full transcript text
            
        Returns:
            Summary object with structured output
        """
        # For now, return a template
        # In actual implementation, this will call Ollama
        
        short_summary = self._generate_short_summary(transcript_text)
        bullet_points = self._generate_bullet_points(transcript_text)
        key_takeaways = self._generate_key_takeaways(transcript_text)
        topics = self._extract_topics(transcript_text)
        
        return Summary(
            short_summary=short_summary,
            bullet_points=bullet_points,
            key_takeaways=key_takeaways,
            topics=topics,
        )
    
    def _generate_short_summary(self, transcript_text: str) -> str:
        """Generate 2-3 sentence summary"""
        prompt = f"""Summarize the following transcript in 2-3 sentences. 
Be concise and capture the main message.

Transcript:
{transcript_text[:2000]}  # Limit to first 2000 chars for speed

Summary:"""
        
        return self._call_ollama(prompt).strip()
    
    def _generate_bullet_points(self, transcript_text: str) -> List[str]:
        """Generate 5-7 key bullet points"""
        prompt = f"""Extract 5-7 key bullet points from the following transcript.
Each bullet should be a complete sentence (10-100 words).
Return only the bullet points, one per line, without numbering.

Transcript:
{transcript_text[:3000]}

Bullet Points:"""
        
        response = self._call_ollama(prompt).strip()
        bullets = [line.strip() for line in response.split("\n") if line.strip()]
        return bullets[:7]  # Limit to 7
    
    def _generate_key_takeaways(self, transcript_text: str) -> List[str]:
        """Generate top 3 key takeaways"""
        prompt = f"""What are the 3 most important takeaways from this transcript?
Format as a list with each takeaway on a new line without numbering.

Transcript:
{transcript_text[:2000]}

Key Takeaways:"""
        
        response = self._call_ollama(prompt).strip()
        takeaways = [line.strip() for line in response.split("\n") if line.strip()]
        return takeaways[:3]
    
    def _extract_topics(self, transcript_text: str) -> List[str]:
        """Extract main topics covered"""
        prompt = f"""List the main topics covered in this transcript.
Return 3-5 topics, one per line, without numbering or bullet points.

Transcript:
{transcript_text[:2000]}

Topics:"""
        
        response = self._call_ollama(prompt).strip()
        topics = [line.strip() for line in response.split("\n") if line.strip()]
        return topics[:5]
    
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
