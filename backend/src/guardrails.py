"""Guardrails to prevent hallucinations and ensure output quality"""

import re
from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel


class GuardrailResult(BaseModel):
    """Result of guardrail validation"""
    is_valid: bool
    confidence: float
    issues: List[str]
    warnings: List[str]


class OutputGuardrails:
    """Guardrails to validate and filter LLM outputs"""
    
    # Hallucination indicators
    HALLUCINATION_PATTERNS = [
        r"i\s+don't\s+know|i\s+don't\s+have",
        r"i\s+cannot\s+find|not\s+found",
        r"unclear|ambiguous",
        r"hypothetical|imagine|suppose",
        r"probably|likely|might|could",
    ]
    
    # Confidence thresholds
    MIN_CONFIDENCE = 0.6
    CONFIDENCE_REDUCTION_PER_ISSUE = 0.1
    
    @staticmethod
    def validate_summary(summary: str) -> GuardrailResult:
        """Validate a generated summary"""
        issues = []
        warnings = []
        confidence = 1.0
        
        # Check for minimum length
        if len(summary.strip()) < 50:
            issues.append("Summary too short (< 50 characters)")
            confidence -= 0.2
        
        # Check for hallucination patterns
        lower_summary = summary.lower()
        for pattern in OutputGuardrails.HALLUCINATION_PATTERNS:
            if re.search(pattern, lower_summary):
                warnings.append(f"Detected uncertainty pattern: {pattern}")
                confidence -= OutputGuardrails.CONFIDENCE_REDUCTION_PER_ISSUE
        
        # Check for incomplete sentences
        if summary.rstrip().endswith(("...", "—", "—", "[")):
            issues.append("Summary appears incomplete")
            confidence -= 0.15
        
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, confidence))
        
        is_valid = confidence >= OutputGuardrails.MIN_CONFIDENCE and not issues
        
        return GuardrailResult(
            is_valid=is_valid,
            confidence=round(confidence, 2),
            issues=issues,
            warnings=warnings
        )
    
    @staticmethod
    def validate_bullet_points(bullets: List[str]) -> GuardrailResult:
        """Validate bullet point list"""
        issues = []
        warnings = []
        confidence = 1.0
        
        # Check for minimum number of bullets
        if len(bullets) < 3:
            issues.append(f"Too few bullet points ({len(bullets)}, expected 5-7)")
            confidence -= 0.2
        elif len(bullets) > 10:
            warnings.append(f"Too many bullet points ({len(bullets)})")
            confidence -= 0.1
        
        # Check each bullet
        for i, bullet in enumerate(bullets):
            if len(bullet.strip()) < 10:
                issues.append(f"Bullet {i+1} too short")
                confidence -= 0.1
            
            if len(bullet.strip()) > 500:
                warnings.append(f"Bullet {i+1} too long")
                confidence -= 0.05
        
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, confidence))
        
        is_valid = confidence >= OutputGuardrails.MIN_CONFIDENCE and not issues
        
        return GuardrailResult(
            is_valid=is_valid,
            confidence=round(confidence, 2),
            issues=issues,
            warnings=warnings
        )
    
    @staticmethod
    def validate_facts(facts: List[str], source_transcript: str) -> GuardrailResult:
        """
        Validate that facts are grounded in source transcript
        """
        issues = []
        warnings = []
        confidence = 1.0
        
        for i, fact in enumerate(facts):
            # Extract key terms from fact
            key_terms = OutputGuardrails._extract_key_terms(fact)
            
            # Check if terms appear in transcript
            found_terms = sum(
                1 for term in key_terms
                if term.lower() in source_transcript.lower()
            )
            
            if found_terms < len(key_terms) * 0.5:
                warnings.append(f"Fact {i+1} partially unsupported by transcript")
                confidence -= 0.15
            elif found_terms == 0:
                issues.append(f"Fact {i+1} not found in transcript")
                confidence -= 0.3
        
        confidence = max(0.0, min(1.0, confidence))
        is_valid = confidence >= OutputGuardrails.MIN_CONFIDENCE and not issues
        
        return GuardrailResult(
            is_valid=is_valid,
            confidence=round(confidence, 2),
            issues=issues,
            warnings=warnings
        )
    
    @staticmethod
    def _extract_key_terms(text: str, min_length: int = 3) -> List[str]:
        """Extract key terms from text (simplified)"""
        # Remove common words and extract terms
        common_words = {
            "the", "a", "an", "is", "are", "was", "were", "be",
            "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "up", "about", "as", "it"
        }
        
        words = text.lower().split()
        return [w.strip(".,!?;:") for w in words 
                if len(w) >= min_length and w.lower() not in common_words]
    
    @staticmethod
    def validate_timestamp_format(timestamps: List[Tuple[str, str]]) -> GuardrailResult:
        """Validate timestamp format (HH:MM:SS -> topic)"""
        issues = []
        warnings = []
        confidence = 1.0
        
        time_pattern = r"^\d{1,2}:\d{2}:\d{2}$"
        
        for i, (timestamp, topic) in enumerate(timestamps):
            if not re.match(time_pattern, timestamp):
                issues.append(f"Invalid timestamp format at position {i+1}: {timestamp}")
                confidence -= 0.2
            
            if not topic or len(topic.strip()) < 3:
                issues.append(f"Missing/invalid topic at timestamp {timestamp}")
                confidence -= 0.15
        
        confidence = max(0.0, min(1.0, confidence))
        is_valid = confidence >= OutputGuardrails.MIN_CONFIDENCE and not issues
        
        return GuardrailResult(
            is_valid=is_valid,
            confidence=round(confidence, 2),
            issues=issues,
            warnings=warnings
        )


class ContentFilter:
    """Filter inappropriate or sensitive content"""
    
    # Patterns for potentially problematic content
    FILTER_PATTERNS = [
        r"(?i)(hate|discriminat|racist|sexist)",
        r"(?i)(violence|weapon|harm)",
    ]
    
    @staticmethod
    def is_appropriate(content: str) -> bool:
        """Check if content is appropriate"""
        for pattern in ContentFilter.FILTER_PATTERNS:
            if re.search(pattern, content):
                return False
        return True
