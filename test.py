"""
Test script to verify the YouTube Analysis Agent system setup
Run this after installing dependencies to ensure everything works
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))

def test_config():
    """Test configuration loading"""
    print("🔧 Testing Configuration...", end=" ")
    try:
        from config import config
        assert config.OLLAMA_BASE_URL
        assert config.OLLAMA_MODEL
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_ollama_connection():
    """Test Ollama connection"""
    print("🔗 Testing Ollama Connection...", end=" ")
    try:
        from config import config
        if not config.validate_ollama_connection():
            print("✗ FAILED: Cannot connect to Ollama")
            print("   Make sure 'ollama serve' is running in another terminal")
            return False
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_transcript_extractor():
    """Test transcript extractor initialization"""
    print("📝 Testing Transcript Extractor...", end=" ")
    try:
        from agents.transcript_extractor import TranscriptExtractor
        extractor = TranscriptExtractor()
        assert extractor.cache_dir
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_summarizer():
    """Test summarizer initialization"""
    print("📋 Testing Content Summarizer...", end=" ")
    try:
        from agents.summarizer import ContentSummarizer
        summarizer = ContentSummarizer()
        assert summarizer.model
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_insight_generator():
    """Test insight generator initialization"""
    print("💡 Testing Insight Generator...", end=" ")
    try:
        from agents.insight_generator import InsightGenerator
        generator = InsightGenerator()
        assert generator.model
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_fact_checker():
    """Test fact checker initialization"""
    print("✓ Testing Fact Checker...", end=" ")
    try:
        from agents.fact_checker import FactChecker
        checker = FactChecker()
        assert checker.model
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_memory():
    """Test memory storage initialization"""
    print("💾 Testing Memory Storage...", end=" ")
    try:
        from config import config
        from memory import MemoryStorage
        memory = MemoryStorage(config.MEMORY_PATH)
        assert memory.storage_path
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_guardrails():
    """Test guardrails"""
    print("🛡️  Testing Guardrails...", end=" ")
    try:
        from guardrails import OutputGuardrails
        result = OutputGuardrails.validate_summary("This is a test summary.")
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'confidence')
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_orchestrator_init():
    """Test orchestrator initialization"""
    print("🎯 Testing Orchestrator...", end=" ")
    try:
        from orchestrator import VideoAnalysisOrchestrator
        orchestrator = VideoAnalysisOrchestrator()
        assert orchestrator.transcript_extractor
        assert orchestrator.summarizer
        assert orchestrator.insight_generator
        assert orchestrator.fact_checker
        assert orchestrator.memory
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def main():
    """Run all tests"""
    os.chdir(Path(__file__).parent / "backend")
    
    print("\n" + "="*60)
    print("YouTube Video Analysis Agent - System Test")
    print("="*60 + "\n")
    
    tests = [
        test_config,
        test_ollama_connection,
        test_transcript_extractor,
        test_summarizer,
        test_insight_generator,
        test_fact_checker,
        test_memory,
        test_guardrails,
        test_orchestrator_init,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("="*60)
        print("\n🎉 Your system is ready! You can now:")
        print("   1. Run the API server: python src/main.py")
        print("   2. Open the web UI: http://localhost:8080")
        print("   3. View API docs: http://localhost:8000/docs")
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print("="*60)
        print("\nPlease fix the errors above and try again.")
        print("See QUICKSTART.md for troubleshooting help.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
