# resume-flow-ai/tests/test_ats_pipeline.py
from unittest.mock import AsyncMock, patch

import pytest

from app.models.ats import LlmAtsAnalysis, RecruiterSimulation, SectionScores
from app.services.ats.ats_pipeline import process_ats_report


@pytest.mark.asyncio
async def test_process_ats_report() -> None:
    mock_llm_response = LlmAtsAnalysis(
        scores=SectionScores(
            formatting=100,
            keywords=100,
            experience=100,
            skills=100,
            impact=100,
            readability=100,
            repetition=100,
            grammar=100,
            parse_rate=100,
        ),
        ats_warnings=[],
        risks=[],
        suggestions=[],
        strong_keywords=[],
        missing_keywords=[],
        feedback=[],
        bullet_reviews=[],
        recruiter_simulation=RecruiterSimulation(
            first_impression="Great", likely_concerns=[], likely_outcome="Yes"
        ),
    )

    with patch(
        "app.services.ats.ats_pipeline.analyze_resume_with_llm", new_callable=AsyncMock
    ) as mock_analyze:
        mock_analyze.return_value = mock_llm_response

        report = await process_ats_report(
            filename="resume.pdf",
            file_bytes=b"dummy",
            raw_text="Contact: a@b.com",
            parsed_data={"name": "Test"},
            job_description=None,
        )

        assert report.overall_score == 100
        assert report.grade == "A+"
        assert report.ats_essentials["pdf_preferred"] is True
