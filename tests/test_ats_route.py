# resume-flow-ai/tests/test_ats_route.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_ats_route():
    with patch("app.routes.resume.parse_resume", new_callable=AsyncMock) as mock_parse, \
         patch("app.routes.resume.process_ats_report", new_callable=AsyncMock) as mock_process:
        
        mock_parse.return_value = ({"name": "Test"}, "Raw text content")
        
        class MockAtsReport:
            def model_dump(self):
                return {"overall_score": 90, "grade": "A"}
                
        mock_process.return_value = MockAtsReport()
        
        response = client.post(
            "/api/v1/resume/ats",
            files={"file": ("test.pdf", b"dummy pdf content", "application/pdf")},
            data={"job_description": "Software Engineer"}
        )
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["success"] is True
        assert json_data["data"]["parsed_resume"]["name"] == "Test"
        assert json_data["data"]["ats_report"]["overall_score"] == 90
