from functools import lru_cache
from pathlib import Path

# Base directory for prompts
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

@lru_cache(maxsize=32)
def load_prompt(path: str) -> str:
    """
    Load a prompt from a markdown file in the prompts directory.
    The path should be relative to the app/prompts directory.
    Example: load_prompt("resume_parser/system.md")
    """
    full_path = PROMPTS_DIR / path
    if not full_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {full_path}")
    
    return full_path.read_text(encoding="utf-8").strip()
