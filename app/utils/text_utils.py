import re

# Common resume section headings and terms
RESUME_KEYWORDS = [
    "experience", "work history", "employment", "exp", "professional history",
    "education", "academic", "school", "university", "edu", "qualification",
    "skills", "technical skills", "competencies", "expertise",
    "projects", "personal projects", "portfolio",
    "summary", "profile", "objective", "about me", "professional summary",
    "certifications", "licenses", "awards", "honors", "achievements",
    "languages", "volunteer", "references", "publications",
    "contact", "links", "linkedin", "github", "address", "phone", "email", "cv", "curriculum vitae"
]

def contains_resume_keywords(text: str, min_score: int = 2) -> bool:
    """
    Check if the text contains common resume keywords or patterns (email/phone).
    Returns True if the 'resume score' meets the minimum threshold.
    """
    if not text:
        return False
    
    text_lower = text.lower()
    score = 0
    
    # 1. Check for keywords (each unique keyword adds 1 to score)
    for keyword in RESUME_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
            score += 1
            if score >= min_score:
                return True
                
    # 2. Check for email/phone (these are strong indicators, each adds 2 to score)
    if extract_emails(text):
        score += 2
    if extract_phone_numbers(text):
        score += 2
        
    return score >= min_score

def extract_emails(text: str) -> list[str]:
    """Extract email addresses from text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str) -> list[str]:
    """Extract phone numbers from text (basic pattern)."""
    # This is a broad pattern for various international formats
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(phone_pattern, text)

def extract_links(text: str) -> list[str]:
    """Extract URLs from text."""
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.findall(url_pattern, text)
