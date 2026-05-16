import logfire
from typing import Any
from huggingface_hub import InferenceClient


from app.core.config import settings

client = InferenceClient(api_key=settings.HF_TOKEN)


def process_field_request(
    action: str,
    fieldName: str,
    originalText: str = "",
    instruction: str = "",
    tone: str = "professional",
    format: str = "paragraph",
    fullResumeData: dict[str, Any] | None = None,
) -> str:
    from app.utils.prompt_loader import load_prompt
    import json

    with logfire.span("process_field_request", action=action, field_name=fieldName):
        system_prompt = load_prompt("field_processor/system.md")

    # Prepare template blocks
    instructions_block = f"Instructions: {instruction}" if instruction else ""
    tone_block = f"Tone: {tone}" if tone else ""
    format_block = "Format as a bulleted list using <ul> and <li> tags." if format == "bullets" else "Format as a paragraph."
    
    resume_context_block = ""
    if fullResumeData:
        # Create a simplified context from the resume data to avoid context window issues
        # and focus on the most relevant parts (experience, projects, skills)
        context_data = {
            "personalInfo": fullResumeData.get("personalInfo", {}),
            "experience": fullResumeData.get("sections", {}).get("experience", {}).get("items", []),
            "skills": fullResumeData.get("sections", {}).get("skills", {}).get("items", []),
            "projects": fullResumeData.get("sections", {}).get("projects", {}).get("items", []),
            "education": fullResumeData.get("sections", {}).get("education", {}).get("items", []),
        }
        resume_context_block = f"\n\nContext from entire resume:\n{json.dumps(context_data, indent=2)}"


    if action == "REWRITE":
        user_prompt_template = load_prompt("field_processor/rewrite.md")
        user_prompt = user_prompt_template.format(
            fieldName=fieldName,
            instructions_block=instructions_block,
            tone_block=tone_block,
            format_block=format_block,
            originalText=originalText,
            resume_context_block=resume_context_block
        )
    else:
        user_prompt_template = load_prompt("field_processor/generate.md")
        user_prompt = user_prompt_template.format(
            fieldName=fieldName,
            instructions_block=instructions_block,
            tone_block=tone_block,
            format_block=format_block,
            resume_context_block=resume_context_block
        )



    # Call the HuggingFace Inference API
    try:
        chat_completion = client.chat_completion(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        content = chat_completion.choices[0].message.content
        if content is None:
            logfire.warning("HF Inference API returned empty content")
            return ""
        
        logfire.info(f"Successfully processed {action} for {fieldName}")
        return content.strip()
    except Exception as e:
        logfire.error(f"HF Inference API call failed: {e}", error=str(e))
        raise e
