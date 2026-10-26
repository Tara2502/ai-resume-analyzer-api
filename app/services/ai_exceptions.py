class AIServiceError(Exception):
    """Base class for exceptions in the AI service."""

class AIRateLimitError(AIServiceError):
    """Raised when the AI provider rate limit is reached."""


class AIUnavailableError(AIServiceError):
    """Raised when the AI provider is temporarily unavailable."""


class AIResponseError(AIServiceError):
    """Raised when the AI provider returns an unusable response."""