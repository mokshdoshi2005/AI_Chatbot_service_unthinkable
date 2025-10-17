import threading
import time
from collections import deque


class SessionService:
    def __init__(self, ttl_seconds=60*60*2): # 2 hours default
        self.sessions = {} # session_id -> { 'history': deque([...]), 'created_at': ts, 'meta': {} }
        self.ttl = ttl_seconds
        self.lock = threading.Lock()
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()


    def get_or_create_session(self, session_id: str):
        with self.lock:
            if session_id not in self.sessions: self.sessions[session_id] = { 'history': deque(maxlen=200), 'created_at': time.time(), 'meta': {'retries': 0} }
            return self.sessions[session_id]


    def add_message(self, session_id: str, role: str, text: str, metadata: dict=None):
        with self.lock:
            s = self.get_or_create_session(session_id)
            s['history'].append({'role': role, 'text': text, 'ts': time.time(), 'meta': metadata or {}})


    def get_context_window(self, session_id: str, window=10):
        with self.lock:
            s = self.get_or_create_session(session_id)
            return list(s['history'])[-window:]


    def _cleanup_loop(self):
        while True:
            now = time.time()
            with self.lock:
                to_delete = []
                for sid, s in list(self.sessions.items()):
                    if now - s['created_at'] > self.ttl: to_delete.append(sid)
                for sid in to_delete:
                    del self.sessions[sid]
            time.sleep(60)




session_service = SessionService()