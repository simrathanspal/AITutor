from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.survey import SurveyQuestion, UserSurveyResponse
from app.services.survey import SurveyService
from app.services.mem0 import Mem0Service
from config import get_settings

router = APIRouter(prefix="/survey", tags=["survey"])

@router.get("/questions", response_model=List[SurveyQuestion])
async def get_survey_questions(
    survey_service: SurveyService = Depends(lambda: SurveyService())
):
    """
    Retrieves all available survey questions.
    Returns a list of questions with their options.
    """
    return survey_service.get_all_questions()

@router.get("/questions/{category}", response_model=List[SurveyQuestion])
async def get_questions_by_category(
    category: str,
    survey_service: SurveyService = Depends(lambda: SurveyService())
):
    """
    Retrieves questions for a specific category.
    Args:
        category: The category of questions to retrieve (e.g., 'learning_format', 'learning_pace')
    Returns:
        List of questions for the specified category
    """
    questions = survey_service.get_questions_by_category(category)
    if not questions:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for category: {category}"
        )
    return questions

@router.post("/submit")
async def submit_survey(
    response: UserSurveyResponse,
    survey_service: SurveyService = Depends(lambda: SurveyService()),
    settings = Depends(get_settings)
):
    """
    Submits survey responses and stores them in Mem0.ai.
    Args:
        response: User's survey responses including user_id and answers
    Returns:
        Processed survey data and initial learning path
    """
    # Process survey responses
    processed_data = survey_service.process_answers(response.dict())
    
    # Store in Mem0.ai and get learning path
    mem0_service = Mem0Service(api_key=settings.MEM0_API_KEY)
    try:
        result = await mem0_service.store_survey_response(
            response.user_id,
            processed_data
        )
        return {
            "status": "success",
            "message": "Survey responses successfully processed",
            "learning_path": result,
            "user_id": response.user_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process survey: {str(e)}"
        )