import re
from typing import Dict, Any, Optional
import re

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
URL_REGEX = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"

def check_essentials(
    filename: Optional[str] = None, 
    file_size_bytes: Optional[int] = None, 
    page_count: Optional[int] = None, 
    raw_text: Optional[str] = None,
    parsed_data: Optional[Dict[str, Any]] = None
) -> Dict[str, bool]:
    # Check for email, phone, and links
    email_valid = False
    phone_valid = False
    links_present = False

    if raw_text:
        email_valid = bool(re.search(EMAIL_REGEX, raw_text))
        phone_valid = bool(re.search(PHONE_REGEX, raw_text))
        links_present = bool(re.search(URL_REGEX, raw_text))
    elif parsed_data:
        # Check in parsed data (assuming reactive-resume schema)
        basics = parsed_data.get("basics", {})
        email_valid = bool(basics.get("email"))
        phone_valid = bool(basics.get("phone"))
        
        # Check profiles for links
        profiles = basics.get("profiles", [])
        links_present = any(p.get("url") for p in profiles) or bool(basics.get("url"))

    return {
        "pdf_preferred": filename.lower().endswith(".pdf") if filename else True,
        "file_size_ok": file_size_bytes < 2 * 1024 * 1024 if file_size_bytes is not None else True,
        "email_valid": email_valid,
        "phone_valid": phone_valid,
        "links_present": links_present,
        "page_count_ok": page_count <= 2 if page_count is not None else True,
    }
