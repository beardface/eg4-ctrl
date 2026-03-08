class EG4Error(Exception):
    """Base exception for EG4 Monitor."""
    pass

class AuthError(EG4Error):
    """Raised when authentication fails."""
    pass

class APIError(EG4Error):
    """Raised when the API returns an error."""
    pass

class SessionError(EG4Error):
    """Raised when there is a session-related error."""
    pass
