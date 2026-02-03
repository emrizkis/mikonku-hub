
import os
import json
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def generate_project_plan(user_prompt):
        """
        Generates a project plan (project details + tasks) based on the user's prompt
        using Google Gemini API. Returns a dictionary.
        """
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            logger.warning("GEMINI_API_KEY not found. Using Mock Response.")
            return AIService._get_mock_response(user_prompt)

        try:
            import google.generativeai as genai
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')

            # Construct the system instruction / prompt
            current_date = datetime.now().strftime("%Y-%m-%d")
            prompt = f"""
            You are an expert Project Manager. Create a detailed project plan based on the following request:
            "{user_prompt}"

            The output must be strictly valid JSON with the following structure:
            {{
                "name": "Project Name",
                "description": "A brief description of the project.",
                "plan_start_date": "YYYY-MM-DD", 
                "plan_end_date": "YYYY-MM-DD",
                "tasks": [
                    {{
                        "name": "Task Name",
                        "start_offset_days": 0,
                        "duration_days": 1
                    }}
                ]
            }}

            Rules:
            1. "plan_start_date" should be the current date: {current_date}.
            2. "plan_end_date" should be calculated based on the total duration of tasks.
            3. "start_offset_days" is the number of days from the project start date when this task begins.
            4. "duration_days" is how long the task takes.
            5. Provide at least 5-10 realistic tasks.
            6. Return ONLY the JSON, no markdown formatting like ```json ... ```.
            """

            response = model.generate_content(prompt)
            
            # Clean up response text if it contains markdown code blocks
            text = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(text)

        except Exception as e:
            logger.error(f"Error generating AI content: {e}")
            # Fallback to mock in case of API failure, or re-raise if strict failure is preferred.
            # For now, let's return a simple error structure or fallback.
            return {
                "error": f"Failed to generate project: {str(e)}"
            }

    @staticmethod
    def _get_mock_response(user_prompt):
        """
        Returns a mock project structure for testing without an API key.
        """
        today = datetime.now()
        start_date_str = today.strftime("%Y-%m-%d")
        end_date_str = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        
        return {
            "name": f"Mock Project: {user_prompt[:20]}...",
            "description": f"This is a generated mock plan for: {user_prompt}",
            "plan_start_date": start_date_str,
            "plan_end_date": end_date_str,
            "tasks": [
                {
                    "name": "Initial Planning Phase",
                    "start_offset_days": 0,
                    "duration_days": 2
                },
                {
                    "name": "Resource Allocation",
                    "start_offset_days": 2,
                    "duration_days": 3
                },
                {
                    "name": "Development Kickoff",
                    "start_offset_days": 5,
                    "duration_days": 5
                },
                {
                    "name": "Final Review",
                    "start_offset_days": 10,
                    "duration_days": 2
                }
            ]
        }
