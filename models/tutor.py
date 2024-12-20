from pydantic import BaseModel
from typing import Optional, Dict, List

class LearningPreferences(BaseModel):
    learning_format: str
    weekly_time: str
    learning_pace: str
    theory_vs_practice: str
    independence_level: str

class LearningSession(BaseModel):
    user_id: str
    topic: str
    session_type: str
    completion_status: str
    feedback: Optional[str]

class LearningPath(BaseModel):
    user_id: str
    current_topic: str
    next_topics: List[str]
    recommendations: Dict[str, str]