import pytest
from app.services.ats.essentials_checker import check_essentials

def test_check_essentials_success():
    raw_text = "Contact me at test@example.com or 555-123-4567. My site: https://github.com/user."
    essentials = check_essentials("resume.pdf", 1024 * 1024, 2, raw_text)
    
    assert essentials["pdf_preferred"] is True
    assert essentials["file_size_ok"] is True
    assert essentials["email_valid"] is True
    assert essentials["phone_valid"] is True
    assert essentials["links_present"] is True
    assert essentials["page_count_ok"] is True

def test_check_essentials_failure():
    raw_text = "No contact info here."
    essentials = check_essentials("resume.docx", 3 * 1024 * 1024, 3, raw_text)
    
    assert essentials["pdf_preferred"] is False
    assert essentials["file_size_ok"] is False
    assert essentials["email_valid"] is False
    assert essentials["phone_valid"] is False
    assert essentials["links_present"] is False
    assert essentials["page_count_ok"] is False
