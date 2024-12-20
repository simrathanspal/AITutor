from mem0ai import MemoryClient
from typing import Dict, Any, List
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Mem0Service:
    def __init__(self, api_key: str):
        self.client = MemoryClient(api_key=api_key)

    async def store_survey_response(self, user_id: str, survey_data: Dict) -> Dict[str, Any]:
        """Stores survey responses in Mem0 memory"""
        try:
            # Format survey data as a dialogue
            messages = [
                {
                    "role": "user",
                    "content": f"My learning preferences from the survey: {json.dumps(survey_data, indent=2)}"
                },
                {
                    "role": "assistant",
                    "content": "I've recorded your learning preferences. I'll use this information to personalize your JavaScript learning experience."
                }
            ]

            # Save to Mem0
            self.client.add(messages, user_id=user_id)

            # Get recommendations based on preferences
            query = "Based on my learning preferences, what should be my learning path for JavaScript?"
            recommendations = self.client.search(query, user_id=user_id)

            return {
                "status": "success",
                "message": "Survey responses saved to memory",
                "recommendations": recommendations
            }

        except Exception as e:
            logger.error(f"Error storing survey response: {str(e)}")
            raise Exception(f"Failed to store survey response: {str(e)}")

    async def get_learning_path(self, user_id: str) -> Dict[str, Any]:
        """Retrieves learning path based on stored preferences"""
        try:
            query = "What is my current learning path and recommendations?"
            results = self.client.search(query, user_id=user_id)
            return {"learning_path": results}
        except Exception as e:
            logger.error(f"Error retrieving learning path: {str(e)}")
            raise Exception(f"Failed to get learning path: {str(e)}")

    async def update_progress(self, user_id: str, topic: str, status: str) -> Dict[str, Any]:
        """Updates progress in Mem0 memory"""
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"I've completed the topic '{topic}' with status: {status}"
                },
                {
                    "role": "assistant",
                    "content": f"Progress updated for topic '{topic}'. I'll adjust recommendations accordingly."
                }
            ]
            
            self.client.add(messages, user_id=user_id)
            return {"status": "success", "message": "Progress updated"}
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
            raise Exception(f"Failed to update progress: {str(e)}")