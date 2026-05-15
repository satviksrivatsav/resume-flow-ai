# resume-flow-ai/tests/test_ats_models.py
from app.models.ats import SectionScores, AtsReport

def test_ats_report_model_initialization():
    scores = SectionScores(
        formatting=80, keywords=70, experience=90, skills=85,
        impact=75, readability=88, repetition=95, grammar=80, parse_rate=100
    )
    report = AtsReport(
        scores=scores,
        ats_warnings=[], risks=[], suggestions=[],
        strong_keywords=[], missing_keywords=[],
        feedback=[], bullet_reviews=[],
        recruiter_simulation={"first_impression": "good", "likely_concerns": [], "likely_outcome": "shortlist"},
        overall_score=85, grade="B", ats_essentials={"pdf_preferred": True}
    )
    assert report.overall_score == 85
    assert report.scores.formatting == 80