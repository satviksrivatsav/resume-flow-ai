# resume-flow-ai/app/services/ats/ats_pipeline.py
from typing import Any, Optional

import fitz
import logfire

from app.models.ats import AtsReport
from app.services.ats.essentials_checker import check_essentials
from app.services.ats.llm_analyzer import analyze_resume_with_llm


def calculate_grade(score: int) -> str:
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 85:
        return "A-"
    if score >= 80:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 70:
        return "B-"
    if score >= 60:
        return "C"
    return "F"


async def process_ats_report(
    filename: Optional[str],
    file_bytes: Optional[bytes],
    raw_text: Optional[str],
    parsed_data: dict[str, Any],
    job_description: str | None,
) -> AtsReport:
    with logfire.span("process_ats_report"):
        page_count = None
        if filename and filename.lower().endswith(".pdf") and file_bytes:
            try:
                with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                    page_count = len(doc)
            except Exception as e:
                logfire.error(f"Failed to open PDF {filename}: {e}")

        file_size = len(file_bytes) if file_bytes else None
        
        essentials = check_essentials(
            filename=filename, 
            file_size_bytes=file_size, 
            page_count=page_count, 
            raw_text=raw_text,
            parsed_data=parsed_data
        )
        
        llm_analysis = await analyze_resume_with_llm(
            parsed_data, raw_text, job_description
        )

        scores = llm_analysis.scores
        # Adjusted weights to include repetition and sum to 1.0
        # formatting(0.1), keywords(0.2), experience(0.15), skills(0.1), 
        # impact(0.15), readability(0.1), repetition(0.05), grammar(0.1), parse_rate(0.05)
        overall_score = int(
            (scores.formatting * 0.10)
            + (scores.keywords * 0.20)
            + (scores.experience * 0.15)
            + (scores.skills * 0.10)
            + (scores.impact * 0.15)
            + (scores.readability * 0.10)
            + (scores.repetition * 0.05)
            + (scores.grammar * 0.10)
            + (scores.parse_rate * 0.05)
        )
        
        # Clamp score between 0 and 100
        overall_score = max(0, min(100, overall_score))

        grade = calculate_grade(overall_score)

        return AtsReport(
            **llm_analysis.model_dump(),
            overall_score=overall_score,
            grade=grade,
            ats_essentials=essentials,
        )
