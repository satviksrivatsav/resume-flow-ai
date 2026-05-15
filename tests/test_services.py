from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.resume import ResumeData
from app.services.field_processor import process_field_request
from app.services.resume_processor import parse_resume, structure_resume_with_llm


@pytest.mark.asyncio
@patch("app.services.resume_processor.structured_parser")
async def test_structure_resume_with_llm(mock_parser):
    # Mock LLM response
    mock_resume_data = ResumeData(
        basics={"name": "John Doe", "email": "john@example.com", "phone": "", "location": "", "url": {"label": "", "href": ""}, "customFields": []},
        summary={"content": "Experienced developer", "visible": True},
        sections={}
    )
    mock_parser.ainvoke = AsyncMock(return_value=mock_resume_data)

    result = await structure_resume_with_llm("Raw resume text")
    
    assert isinstance(result, ResumeData)
    assert result.basics.name == "John Doe"
    mock_parser.ainvoke.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.resume_processor.ContentExtractor.extract_text_from_pdf")
@patch("app.services.resume_processor.structure_resume_with_llm")
@patch("app.services.resume_processor.is_valid_resume_file")
@patch("app.services.resume_processor.ContentExtractor.validate_content_quality")
async def test_parse_resume_pdf(mock_quality, mock_valid, mock_structure, mock_extract):
    mock_valid.return_value = (True, None)
    mock_extract.return_value = "Extracted text"
    mock_quality.return_value = True
    
    mock_resume_data = MagicMock(spec=ResumeData)
    mock_resume_data.model_dump.return_value = {"basics": {"name": "John Doe"}}
    mock_structure.return_value = mock_resume_data

    # Use a dummy filename that ends with .pdf
    result, text = await parse_resume(b"pdf_bytes", "test.pdf")

    assert isinstance(result, dict)
    assert result["basics"]["name"] == "John Doe"
    assert text == "Extracted text"

    mock_extract.assert_called_once()
    mock_structure.assert_called_once_with("Extracted text")

@patch("app.services.field_processor.client.chat_completion")
@patch("app.utils.prompt_loader.load_prompt")
def test_process_field_request_rewrite(mock_load_prompt, mock_chat):
    mock_load_prompt.return_value = "System prompt"
    # Mock HF response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Improved text"
    mock_chat.return_value = mock_response

    result = process_field_request(
        action="REWRITE",
        fieldName="Summary",
        originalText="old text",
        tone="professional"
    )

    assert result == "Improved text"
    mock_chat.assert_called_once()
