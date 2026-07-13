import asyncio
import json
from typing import Dict, List, Optional

# ==========================================
# HARDCODED STRUCTURAL MATRICES
# ==========================================

EVALUATION_MATRIX = {
    "behavioral": {
        "star_method": "Must explicitly contain Situation, Task, Action, and Result.",
        "empathy_index": "Evaluates tone for emotional intelligence and conflict resolution.",
        "leadership": "Looks for proactive ownership vs passive participation."
    },
    "technical": {
        "accuracy": "Factual correctness of the technical concept.",
        "clarity": "Ability to explain complex systems simply (the Feynman technique).",
        "boundary_awareness": "Acknowledging what they DO NOT know, rather than guessing."
    }
}

DRESS_CODE_MATRIX_2026 = {
    "hybrid_remote": {
        "description": "Camera-ready top half, structured but comfortable bottom.",
        "guidelines": "Solid colors avoid camera strobing. Ring light awareness. Clean background."
    },
    "formal_corporate": {
        "description": "Traditional high-stakes finance/law presentation.",
        "guidelines": "Tailored suit in navy/charcoal. Minimal jewelry. Crisp collar."
    },
    "tech_casual": {
        "description": "Startups and tech enterprise (Silicon Valley standard).",
        "guidelines": "Premium basics. Unbranded dark t-shirt or crisp button-down, dark denim. Grooming must be immaculate to offset casual clothing."
    }
}

PSYCHOLOGICAL_GROUNDING_MATRIX = {
    "box_breathing": "Inhale 4s, Hold 4s, Exhale 4s, Hold 4s. Repeat 3x to lower cortisol.",
    "cognitive_reframe": "Shift internal narrative from 'I must impress them' to 'We are figuring out if we want to work together'.",
    "sensory_anchor": "Find 3 physical objects in the room and name their colors mentally to stop anxiety spiraling."
}

# ==========================================
# AGENT CLASS LOGIC
# ==========================================

class InterviewTutorAgent:
    def __init__(self, api_key: str = None):
        """
        Initializes the tutor. In a real environment, you pass the Gemini/LLM API key here.
        """
        self.api_key = api_key
        # Track session state to prevent infinite limit-breaking loops
        self.max_questions_per_session = 5
        self.current_question_count = 0

    async def _mock_llm_evaluation(self, job_description: str, question: str, user_answer: str) -> Dict:
        """
        Internal method: Simulates the LLM call. 
        Replace this with actual Google Gemini async API call logic.
        """
        # Simulate network delay without blocking the main thread
        await asyncio.sleep(1.5) 
        
        # This simulates the structured output your AI model should return
        return {
            "score": 78,
            "strengths": ["Clear action taken", "Good technical vocabulary"],
            "weaknesses": ["Forgot to mention the final result (Failed STAR method)"],
            "actionable_fix": "Add one sentence at the end explaining how your action improved metrics by X%."
        }

    async def process_answer(self, job_description: str, company_culture: str, question: str, user_answer: str) -> str:
        """
        The main asynchronous processor for evaluating a user's interview answer.
        """
        if self.current_question_count >= self.max_questions_per_session:
            return json.dumps({"error": "Session limit reached. Please start a new interview."})

        self.current_question_count += 1

        try:
            # 1. Fetch LLM evaluation concurrently
            evaluation = await self._mock_llm_evaluation(job_description, question, user_answer)

            # 2. Select appropriate dress code advice based on culture
            dress_advice = DRESS_CODE_MATRIX_2026.get(
                company_culture.lower(), 
                DRESS_CODE_MATRIX_2026["hybrid_remote"] # Default fallback
            )

            # 3. Assemble the structured feedback loop
            feedback_loop = {
                "evaluation_metrics": {
                    "overall_score": evaluation["score"],
                    "strengths": evaluation["strengths"],
                    "areas_to_improve": evaluation["weaknesses"],
                    "how_to_say_it_better": evaluation["actionable_fix"]
                },
                "coaching_frameworks_applied": {
                    "behavioral_check": EVALUATION_MATRIX["behavioral"]["star_method"],
                    "technical_check": EVALUATION_MATRIX["technical"]["clarity"]
                },
                "pre_interview_prep": {
                    "recommended_attire": dress_advice,
                    "nerve_settler": PSYCHOLOGICAL_GROUNDING_MATRIX["box_breathing"]
                }
            }

            return json.dumps(feedback_loop, indent=2)

        except Exception as e:
            return json.dumps({"error": f"Evaluation failed: {str(e)}"})

# ==========================================
# EXECUTION (HOW TO RUN THIS SAFELY)
# ==========================================

async def main():
    # Instantiate the agent
    tutor = InterviewTutorAgent()
    
    # Mock Data (This would come from your Next.js/Vercel frontend)
    job_desc = "Senior Python Developer focusing on scalable async APIs."
    culture = "tech_casual"
    question = "Tell me about a time your code crashed in production."
    answer = "The server went down because I wrote an infinite loop. I quickly found the loop and deleted it. Then everything was fine."

    print("Evaluating answer asynchronously (No infinite loops)...\n")
    
    # Process the evaluation safely
    result = await tutor.process_answer(
        job_description=job_desc,
        company_culture=culture,
        question=question,
        user_answer=answer
    )
    
    print(result)

if __name__ == "__main__":
    # Standard Python async execution entry point
    asyncio.run(main())
