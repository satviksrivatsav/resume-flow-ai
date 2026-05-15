import pytest
from unittest.mock import patch, AsyncMock
from app.services.ats.llm_analyzer import analyze_resume_with_llm
from app.models.ats import LlmAtsAnalysis, SectionScores, RecruiterSimulation

@pytest.mark.asyncio
async def test_analyze_resume_with_llm():
    mock_response = LlmAtsAnalysis(
        scores=SectionScores(formatting=80, keywords=80, experience=80, skills=80, impact=80, readability=80, repetition=80, grammar=80, parse_rate=80),
        ats_warnings=["warning 1"],
        risks=[], suggestions=[], strong_keywords=[], missing_keywords=[],
        feedback=[], bullet_reviews=[],
        recruiter_simulation=RecruiterSimulation(first_impression="Good", likely_concerns=[], likely_outcome="Yes"),
        jd_match=None
    )
    
    with patch("app.services.ats.llm_analyzer.structured_parser") as mock_parser:
        mock_parser.ainvoke = AsyncMock(return_value=mock_response)
        
        result = await analyze_resume_with_llm({"name": "Test"}, "Raw resume text", None)
        
        assert result.ats_warnings == ["warning 1"]
        mock_parser.ainvoke.assert_called_once()
