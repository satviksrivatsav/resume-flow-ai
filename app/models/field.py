from pydantic import BaseModel, field_validator
from typing import Optional, Literal

class Field(BaseModel):
    """"Data model of a Field request."""
    action: Literal['REWRITE', 'GENERATE']
    fieldName: str
    originalText: Optional[str] = ""
    instruction: Optional[str] = ""
    tone: Literal['professional', 'casual', 'confident', 'friendly'] = "professional"
    format: Literal['bullets', 'paragraph'] = "paragraph"

    @field_validator('tone', 'format', mode='before')
    @classmethod
    def empty_string_to_default(cls, v, info):
        """Convert empty strings to the field's default value."""
        if v == "":
            return cls.model_fields[info.field_name].default
        return v

class FieldMeta(BaseModel):
    """Metadata for fields"""
    processingTimeMs: int
    action: str
    fieldName: str

class FieldResponse(BaseModel):
    """Response object model for field requests"""
    id: str
    newText: str = ""
    meta: FieldMeta