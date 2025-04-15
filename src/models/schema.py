from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class TutorialLink(BaseModel):
    """Model for a tutorial link in the sidebar"""
    title: str
    url: str


class CodeExample(BaseModel):
    """Model for a code example"""
    language: str = "javascript"  # Default language
    code: str


class TutorialContent(BaseModel):
    """Model for the content of a tutorial page"""
    title: str
    url: str
    content: str
    code_examples: List[CodeExample] = []
    next_link: Optional[str] = None

    @validator('content')
    def content_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('content cannot be empty')
        return v


class TutorialCourse(BaseModel):
    """Model for the entire tutorial course"""
    title: str
    source_url: str
    modules: List[TutorialLink]
    tutorials: List[TutorialContent]
    metadata: Dict[str, Any] = Field(default_factory=dict)