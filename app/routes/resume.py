import logging
import time
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.field import Field, FieldResponse
from app.services.field_processor import process_field_request
from app.services.resume_parser import parse_resume_pdf

router = APIRouter(prefix="/resume", tags=["Resume"])
logger = logging.getLogger(__name__)


@router.post("/parse")
async def parse_resume(file: Annotated[UploadFile, File(...)]):
    """
    Parse a PDF resume and extract structured data.
    
    Returns ResumeData matching the frontend type structure.
    """
    # Validate file type
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    try:
        # Read file bytes
        pdf_bytes = await file.read()
        
        # Parse resume
        resume_data = await parse_resume_pdf(pdf_bytes)
        
        return {
            "success": True,
            "data": resume_data
        }
    except ValueError as e:
        logger.warning(f"Resume parsing failed: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Failed to parse resume")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post(path="/field")
async def field_action(request: Field):
    """
        Process field level requests
    """

    # Mark the start time
    starting_time = time.time()

    # Validate the fields first
    if not request.action or request.action not in ['REWRITE', 'GENERATE']:
        raise HTTPException(status_code=400, detail="No Field action detected or Invalid action")

    if not request.fieldName:
        raise HTTPException(status_code=400, detail="Invalid Resume Field or No field name detected")

    if request.action == 'REWRITE' and not request.originalText:
        raise HTTPException(status_code=400, detail="No existing text detected to perform REWRITE action")

    # Process field request
    try:
        processed_field = process_field_request(**request.model_dump())
        time_taken = (time.time() - starting_time) * 1000
        response = FieldResponse(
            id="0",
            newText=processed_field,
            meta={
                "processingTimeMs": int(time_taken),
                "action": request.action,
                "fieldName": request.fieldName
            }
        )

        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        logger.exception("Failed to process field")
        raise HTTPException(status_code=500, detail=str(e)) from e