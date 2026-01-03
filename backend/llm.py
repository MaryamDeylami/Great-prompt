import openai
import os
from dotenv import load_dotenv

load_dotenv("E:/daneshgah/narm afzar/project/backend/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env")


def get_ai_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Generate a response from the AI model based on the given prompt.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=15
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "خطا در ارتباط با AI. دوباره تلاش کنید."
