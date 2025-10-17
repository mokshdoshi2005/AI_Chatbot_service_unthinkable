import os
import time
from typing import List


OPENAI_KEY = os.getenv('OPENAI_API_KEY')


# lightweight LLM service with fallback behavior
class LLMService:
    def __init__(self):
        self.provider = 'openai' if OPENAI_KEY else 'stub'


    def build_prompt(self, context: List[dict], faqs: List[dict], query: str) -> str:
        ctx = '\n'.join([f"{m['role']}: {m['text']}" for m in context])
        faq_text = '\n'.join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
        prompt = f"You are a helpful customer support assistant.\n\nContext:\n{ctx}\n\nRelevant FAQs:\n{faq_text}\n\nUser Query:\n{query}\n\nProvide a concise answer and a confidence score between 0 and 1.\n"
        return prompt


    def generate_response(self, prompt: str) -> dict:
        # If OpenAI key present, call OpenAI (simple completion). Otherwise return a safe stub.
        if self.provider == 'openai':
            try:
                import openai
                openai.api_key = OPENAI_KEY
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini' if hasattr(openai, 'ChatCompletion') else 'gpt-3.5-turbo',
                    messages=[{'role': 'system', 'content': prompt}],
                    max_tokens=300,
                    temperature=0.0,
                )
                text = resp['choices'][0]['message']['content'].strip()
                # naive parse: expects last line like "Confidence: 0.85"
                confidence = 0.5
                lines = text.splitlines()
                for l in reversed(lines[-3:]):
                    if 'confidence' in l.lower():
                        try: confidence = float(''.join(ch for ch in l if (ch.isdigit() or ch=='.')))
                        except: confidence = 0.5
                return {'answer': text, 'confidence': confidence}
            except Exception as e:
                # On error, fall back to stub
                return self._stub_response(prompt)
        else:
            return self._stub_response(prompt)


    def _stub_response(self, prompt: str) -> dict:
        # Very simple heuristic: if 'password' in prompt -> answer accordingly
        if 'password' in prompt.lower():
            answer = "To reset your password, click 'Forgot Password' on the login page and follow the instructions emailed to you."
            confidence = 0.95
        else:
            answer = "I'm sorry — I don't have enough information to answer that confidently. Please provide more details or contact support."
            confidence = 0.35
        # include timestamp
        return {'answer': answer, 'confidence': confidence}




llm_service = LLMService()