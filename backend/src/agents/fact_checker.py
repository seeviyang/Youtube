"""Fact Checker Agent - Validates facts and generates confidence scores"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from ..guardrails import OutputGuardrails
from ..config import config


@dataclass
class FactCheckResult:
    """Result of fact checking"""
    claim: str
    supported: bool
    confidence: float
    evidence: str  # Reference to transcript segment
    timestamp: str


class FactChecker:
    """Validates facts against source transcript"""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize fact checker"""
        self.model = model or config.OLLAMA_MODEL
        self.base_url = config.OLLAMA_BASE_URL
    
    def check_facts(
        self,
        claims: List[str],
        transcript_text: str,
        transcript_segments: Optional[List] = None,
    ) -> List[FactCheckResult]:
        """
        Check facts against transcript
        
        Args:
            claims: List of claims to verify
            transcript_text: Full transcript text
            transcript_segments: Optional list of transcript segments with timestamps
            
        Returns:
            List of FactCheckResult objects
        """
        results = []
        
        for claim in claims:
            result = self._check_single_fact(
                claim,
                transcript_text,
                transcript_segments
            )
            results.append(result)
        
        return results
    
    def _check_single_fact(
        self,
        claim: str,
        transcript_text: str,
        transcript_segments: Optional[List] = None,
    ) -> FactCheckResult:
        """Check a single fact"""
        
        # Basic validation using guardrails
        guardrail_result = OutputGuardrails.validate_facts(
            [claim],
            transcript_text
        )
        
        # Find supporting evidence
        evidence, timestamp = self._find_supporting_evidence(
            claim,
            transcript_text,
            transcript_segments
        )
        
        # Calculate confidence based on evidence
        confidence = guardrail_result.confidence
        if not evidence:
            confidence = max(0.2, confidence - 0.3)
        
        return FactCheckResult(
            claim=claim,
            supported=guardrail_result.is_valid,
            confidence=confidence,
            evidence=evidence,
            timestamp=timestamp,
        )
    
    def _find_supporting_evidence(
        self,
        claim: str,
        transcript_text: str,
        transcript_segments: Optional[List] = None,
    ) -> Tuple[str, str]:
        """Find supporting evidence for a claim in transcript"""
        
        # Extract key terms from claim
        key_terms = OutputGuardrails._extract_key_terms(claim)
        
        best_match = ""
        best_timestamp = "00:00:00"
        best_score = 0
        
        if transcript_segments:
            # Search through segments
            for segment in transcript_segments:
                score = sum(
                    1 for term in key_terms
                    if term.lower() in segment.text.lower()
                )
                
                if score > best_score:
                    best_score = score
                    best_match = segment.text
                    best_timestamp = segment.timestamp
        else:
            # Search through transcript text by sentences
            sentences = transcript_text.split(".")
            for sentence in sentences:
                score = sum(
                    1 for term in key_terms
                    if term.lower() in sentence.lower()
                )
                
                if score > best_score:
                    best_score = score
                    best_match = sentence.strip()
        
        return best_match, best_timestamp
    
    def generate_confidence_summary(self, fact_checks: List[FactCheckResult]) -> Dict:
        """Generate summary of fact-check results"""
        
        total = len(fact_checks)
        supported = sum(1 for fc in fact_checks if fc.supported)
        avg_confidence = (
            sum(fc.confidence for fc in fact_checks) / total
            if total > 0 else 0
        )
        
        return {
            "total_facts_checked": total,
            "supported_facts": supported,
            "unsupported_facts": total - supported,
            "support_percentage": round((supported / total * 100) if total > 0 else 0, 1),
            "average_confidence": round(avg_confidence, 2),
            "findings": [
                {
                    "claim": fc.claim,
                    "supported": fc.supported,
                    "confidence": fc.confidence,
                    "evidence": fc.evidence[:100] + "..." if len(fc.evidence) > 100 else fc.evidence,
                    "timestamp": fc.timestamp,
                }
                for fc in fact_checks
            ]
        }
