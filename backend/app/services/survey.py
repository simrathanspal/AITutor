from typing import List, Dict
from app.models.survey import SurveyQuestion, SurveyOption

class SurveyService:
    def __init__(self):
        self.questions = [
            SurveyQuestion(
                id=1,
                category="learning_format",
                question="What's the best way for you to receive information during learning?",
                options=[
                    SurveyOption(id=1, text="Text-based guide with examples"),
                    SurveyOption(id=2, text="Video with step-by-step explanations"),
                    SurveyOption(id=3, text="Practical tasks to solve on your own"),
                    SurveyOption(id=4, text="Combined format (all options together)")
                ]
            ),
            SurveyQuestion(
                id=2,
                category="learning_pace",
                question="How much time per week can you dedicate to learning?",
                options=[
                    SurveyOption(id=1, text="Less than 3 hours"),
                    SurveyOption(id=2, text="3-5 hours"),
                    SurveyOption(id=3, text="5-10 hours"),
                    SurveyOption(id=4, text="More than 10 hours")
                ]
            ),
            SurveyQuestion(
                id=3,
                category="learning_style",
                question="What learning pace do you prefer?",
                options=[
                    SurveyOption(id=1, text="Fast-paced (intensive material coverage)"),
                    SurveyOption(id=2, text="Balanced (mix of learning and breaks)"),
                    SurveyOption(id=3, text="Slow-paced (step-by-step learning)")
                ]
            ),
            SurveyQuestion(
                id=4,
                category="theory_practice",
                question="How do you prefer to learn new concepts?",
                options=[
                    SurveyOption(id=1, text="Read theory first, then practice"),
                    SurveyOption(id=2, text="Learn by doing, reference theory as needed")
                ]
            )
        ]

    def get_all_questions(self) -> List[SurveyQuestion]:
        """Retrieves all survey questions"""
        return self.questions

    def get_questions_by_category(self, category: str) -> List[SurveyQuestion]:
        """Retrieves questions filtered by category"""
        return [q for q in self.questions if q.category == category]

    def validate_answer(self, question_id: int, option_id: int) -> bool:
        """Validates if the answer option exists for the given question"""
        question = next((q for q in self.questions if q.id == question_id), None)
        if not question:
            return False
        return any(opt.id == option_id for opt in question.options)

    def process_answers(self, answers: Dict) -> Dict:
        """Processes survey answers and formats data for Mem0.ai storage"""
        processed_data = {
            "learning_preferences": {},
            "metadata": {
                "timestamp": "2024-01-01T00:00:00Z",
                "survey_version": "1.0"
            }
        }
        
        for answer in answers["answers"]:
            question = next(q for q in self.questions if q.id == answer["question_id"])
            option = next(opt for opt in question.options if opt.id == answer["selected_option_id"])
            processed_data["learning_preferences"][question.category] = {
                "selected_option": option.text,
                "question_id": question.id
            }
            
        return processed_data