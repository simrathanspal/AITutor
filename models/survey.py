from pydantic import BaseModel
from typing import List, Optional

class SurveyOption(BaseModel):
    id: int
    text: str

class SurveyQuestion(BaseModel):
    id: int
    question: str
    options: List[SurveyOption]
    category: str

class UserAnswer(BaseModel):
    question_id: int
    selected_option_id: int

class UserSurveyResponse(BaseModel):
    user_id: str
    answers: List[UserAnswer]