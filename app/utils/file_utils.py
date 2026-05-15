
import filetype


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """Check if the file extension is in the allowed list."""
    if not filename:
        return False
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def validate_mime_type(file_bytes: bytes, expected_mimes: list[str]) -> bool:
    """
    Validate the file's MIME type using magic bytes.
    Returns True if the MIME type is in the expected list.
    """
    kind = filetype.guess(file_bytes)
    if kind is None:
        # Fallback for some plain text files or unknown types
        return False
    return kind.mime in expected_mimes

def get_file_size_mb(file_bytes: bytes) -> float:
    """Return the file size in megabytes."""
    return len(file_bytes) / (1024 * 1024)

def is_valid_resume_file(file_bytes: bytes, filename: str, max_size_mb: float = 10.0) -> tuple[bool, str | None]:
    """
    Comprehensive file validation: extension, size, and MIME.
    Returns (is_valid, error_message).
    """
    allowed_exts = [".pdf", ".docx", ".png", ".jpg", ".jpeg", ".txt"]
    allowed_mimes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/png",
        "image/jpeg",
        "text/plain",
    ]

    if not validate_file_extension(filename, allowed_exts):
        return False, f"Unsupported file extension. Allowed: {', '.join(allowed_exts)}"

    if len(file_bytes) == 0:
        ext = filename.split('.')[-1] if '.' in filename else "unknown"
        return False, f"The file is empty and does not match the .{ext} extension."

    if get_file_size_mb(file_bytes) > max_size_mb:
        return False, f"File size exceeds the limit of {max_size_mb}MB"

    kind = filetype.guess(file_bytes)
    
    # Text files usually return None for magic bytes
    if kind is None:
        if filename.lower().endswith(".txt"):
            return True, None
        return False, "File identity mismatch: The content is not a valid document or image."

    # Map extensions to expected MIME categories
    mime = kind.mime
    if filename.lower().endswith(".pdf") and mime != "application/pdf":
        return False, f"File identifies as {mime}, but expected PDF."
    
    if filename.lower().endswith(".docx") and mime not in ["application/zip", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return False, f"File identifies as {mime}, but expected DOCX (ZIP)."
    
    if any(filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]) and not mime.startswith("image/"):
        return False, f"File identifies as {mime}, but expected Image."

    # Final allowed list check
    if mime not in allowed_mimes and mime != "application/zip":
         return False, f"Unsupported file content type: {mime}"
    
    # Extra check for PDF header
    if filename.lower().endswith(".pdf") and not file_bytes.startswith(b"%PDF-"):
        return False, "Invalid PDF header detected."

    return True, None
