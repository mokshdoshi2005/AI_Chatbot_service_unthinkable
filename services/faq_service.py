import json
import os
from typing import List


DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')


class FAQService:
    def __init__(self, path=DATA_PATH):
        with open(path, 'r', encoding='utf-8') as f: self.faqs = json.load(f)


    def find_relevant(self, query: str, top_k=3) -> List[dict]:
        # Simple keyword match scoring; replace with semantic search later
        q = query.lower()
        scored = []
        for f in self.faqs:
            score = 0
            for kw in f.get('keywords', []):
                if kw.lower() in q: score += 1
            if score > 0: scored.append((score, f))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [f for s, f in scored[:top_k]]




faq_service = FAQService()