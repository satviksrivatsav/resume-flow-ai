import logfire
from typing import Any, cast, Optional
from app.models.ats import LlmAtsAnalysis
from app.services.resume_processor import base_llm

structured_parser = base_llm.with_structured_output(
    LlmAtsAnalysis,
    method="json_mode",
    strict=True
)

async def analyze_resume_with_llm(
    parsed_data: dict[str, Any], raw_text: Optional[str] = None, job_description: str | None = None
) -> LlmAtsAnalysis:
    from app.utils.prompt_loader import load_prompt

    with logfire.span("analyze_resume_with_llm"):
        system_prompt = load_prompt("ats/system.md")
        user_prompt_template = load_prompt("ats/user.md")
        
        jd_section = ""
        if job_description:
            jd_section = f"### Job Description:\n{job_description}"
            
        user_prompt = user_prompt_template.format(
            parsed_data=parsed_data,
            raw_text=raw_text or "No raw text available (analyzing structured data only)",
            job_description_section=jd_section
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = await structured_parser.ainvoke(messages)
            return cast(LlmAtsAnalysis, response)
        except Exception as e:
            logfire.error(f"LLM ATS Analysis failed: {e}", error=str(e))
            raise ValueError(f"LLM ATS Analysis failed: {e}") from e
