# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Shared Groq client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# class BaseAgent:
#     def __init__(self, model="llama-3.3-70b-versatile"):
#         self.model = model

#     def ask(self, prompt: str):
#         """Send text to Groq LLM."""
#         response = client.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response.choices[0].message.content

import json
from groq import Groq

class BaseAgent:
    def __init__(self):
        self.client = Groq()

    def ask(self, prompt: str):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content

        # --- SANITIZE MODEL OUTPUT ---
        cleaned = (
            raw.replace("```json", "")
               .replace("```", "")
               .replace("\n", " ")
        )

        # --- TRY PARSE ---
        try:
            return json.loads(cleaned)
        except:
            # Auto-fix common issues
            try:
                cleaned = cleaned.strip()
                if cleaned.startswith("{") and cleaned.endswith("}"):
                    return json.loads(cleaned)
            except:
                pass

        # If still failing → wrap in a JSON object
        return {"raw_text": cleaned, "error": "Invalid JSON returned from model"}
