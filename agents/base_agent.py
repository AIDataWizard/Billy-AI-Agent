from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Shared Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class BaseAgent:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.model = model

    def ask(self, prompt: str):
        """Send text to Groq LLM."""
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
