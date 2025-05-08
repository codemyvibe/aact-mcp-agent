"""Session management for the AACT Query Agent."""

from google.adk.sessions import InMemorySessionService
from .config import APP_NAME

# Session service instance
session_service = InMemorySessionService()

def get_or_create_session(user_id, session_id=None):
    """Get an existing session or create a new one.
    
    Args:
        user_id: The ID of the user.
        session_id: Optional session ID. If None, one will be generated.
        
    Returns:
        The session object.
    """
    if session_id is None:
        session_id = f"session_{user_id}"
        
    try:
        session = session_service.get_session(APP_NAME, user_id, session_id)
    except KeyError:
        session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state={}
        )
        
    return session_service.get_session(APP_NAME, user_id, session_id) 