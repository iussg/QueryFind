import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMError(Exception):
    pass

class GroqClient:
    def __init__(self, model="llama-3.3-70b-versatile", temperature=0.1, max_tokens=1000):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMError("GROQ_API_KEY not found in .env file")
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, system_prompt: str, user_message: str) -> str:
        for attempt in range(2):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if 'rate_limit' in str(e).lower() and attempt == 0:
                    print("Rate limit hit. Waiting 30 seconds...")
                    time.sleep(30)
                else:
                    raise LLMError(f"Groq API error: {str(e)}")

    def generate_sql(self, system_prompt: str, user_message: str) -> str:
        raw = self.generate(system_prompt, user_message)
        # Strip markdown code fences
        if '```sql' in raw:
            raw = raw.split('```sql')[1].split('```')[0]
        elif '```' in raw:
            raw = raw.split('```')[1].split('```')[0]
        return raw.strip()

if __name__ == '__main__':
    client = GroqClient()
    result = client.generate("You are a helpful assistant.", "Say hello in one word")
    print("Groq response:", result)