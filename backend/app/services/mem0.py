import aiohttp
from typing import Dict, Any, Optional
import json

class Mem0Service:
    def __init__(self, api_key: str, base_url: str = "https://api.mem0.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def store_survey_response(self, user_id: str, survey_data: Dict) -> Dict[str, Any]:
        """Stores survey responses in Mem0.ai"""
        prompt = f"""
        Analyze the learning preferences for user {user_id}:
        {json.dumps(survey_data, indent=2)}
        
        Based on these preferences, create a personalized learning path and provide recommendations.
        Include:
        1. Suggested learning format
        2. Recommended pace
        3. Theory/practice balance
        4. Initial topics to cover
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/store",
                headers=self.headers,
                json={
                    "user_id": user_id,
                    "content": survey_data,
                    "metadata": {"type": "survey_response"}
                }
            ) as response:
                return await response.json()

    async def get_learning_path(self, user_id: str) -> Dict[str, Any]:
        """Retrieves personalized learning path based on survey responses"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/users/{user_id}/learning_path",
                headers=self.headers
            ) as response:
                return await response.json()

    async def update_progress(self, user_id: str, progress_data: Dict) -> Dict[str, Any]:
        """Updates learning progress and gets recommendations"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/users/{user_id}/progress",
                headers=self.headers,
                json=progress_data
            ) as response:
                return await response.json()
            