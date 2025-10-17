ESCALATION_KEYWORDS = ['refund', 'cancel', 'manager', 'complain', 'sue']


class EscalationService:
    def __init__(self, low_confidence_threshold=0.4, retry_threshold=3):
        self.low_confidence_threshold = low_confidence_threshold
        self.retry_threshold = retry_threshold


    def should_escalate(self, answer: str, confidence: float, user_message: str, session: dict):
        # Check confidence
        if confidence < self.low_confidence_threshold:
            # increment retries
            session['meta']['retries'] = session['meta'].get('retries', 0) + 1
            if session['meta']['retries'] >= self.retry_threshold: return True, 'low_confidence_retries'
            return False, 'low_confidence'


        # Check keywords
        lm = user_message.lower()
        for kw in ESCALATION_KEYWORDS:
            if kw in lm:return True, f'keyword:{kw}'


        # Otherwise no escalation
        session['meta']['retries'] = 0
        return False, ''




escalation_service = EscalationService()