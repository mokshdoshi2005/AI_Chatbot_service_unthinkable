from flask import Blueprint, request, jsonify
from services.session_service import session_service
from services.faq_service import faq_service
from services.llm_service import llm_service
from services.escalation_service import escalation_service


chat_bp = Blueprint('chat', __name__)




@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    session_id = data.get('session_id')
    message = data.get('message')


    if not session_id or not message:
        return jsonify({'error': 'session_id and message are required'}), 400


    session = session_service.get_or_create_session(session_id)
    # Save user message
    session_service.add_message(session_id, 'user', message)


    # Get context window
    context = session_service.get_context_window(session_id, window=10)


    # Get relevant FAQs
    faqs = faq_service.find_relevant(message, top_k=3)


    # Build prompt and call LLM
    prompt = llm_service.build_prompt(context, faqs, message)
    result = llm_service.generate_response(prompt)


    # result = { 'answer': str, 'confidence': float }
    answer = result.get('answer')
    confidence = result.get('confidence', 0.0)


    # Escalation decision
    escalated, reason = escalation_service.should_escalate(answer, confidence, message, session)


    # Save bot response
    session_service.add_message(session_id, 'bot', answer, metadata={'confidence': confidence, 'escalated': escalated})


    return jsonify({
        'response': answer,
        'confidence': confidence,
        'escalated': escalated,
        'escalation_reason': reason
    })