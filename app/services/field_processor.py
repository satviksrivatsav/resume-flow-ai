import logging

from huggingface_hub import InferenceClient

from app.core.config import settings

logger = logging.getLogger(__name__)
client = InferenceClient(api_key=settings.HF_TOKEN)

def process_field_request(action: str, fieldName: str, originalText: str = "", instruction: str = "", tone: str = "professional", format: str = "paragraph"):
    # Build a System prompt
    system_prompt = "You are a professional resume writer. Generate professional resume content. Be concise, impactful, and use action verbs. Return ONLY the improved text, no explanations."

    # Build user prompt
    if action == "REWRITE":
        user_prompt = f"""Rewrite the following text for a resume {fieldName} field.
        {f"Instructions: {instruction}" if instruction else ""}
        {f"Tone: {tone}" if tone else ""}
        {"Format as bullet points (start each with •)." if format == "bullets" else "Format as a paragraph."}

        Text to rewrite:
        "{originalText}"

        Respond with ONLY the rewritten text."""
    else:
        user_prompt = f"""Generate content for a resume {fieldName} field.
        {f"Instructions: {instruction}" if instruction else ""}
        {f"Tone: {tone}" if tone else ""}
        {"Format as bullet points (start each with •)." if format == "bullets" else "Format as a paragraph."}

        Respond with ONLY the generated text."""

    # Call the HuggingFace Inference API
    chat_completion = client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )

    return chat_completion.choices[0].message.content.strip()